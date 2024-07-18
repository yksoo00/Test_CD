import os
import edge_tts
import librosa
import soundfile as sf
import subprocess
import asyncio
from scipy.io import wavfile
from scipy.signal import resample
from celery import Celery
from openai import OpenAI
from langchain.prompts import PromptTemplate
from pydub import AudioSegment
import io
import base64


broker_url = os.getenv("CELERY_BROKER_URL")
app = Celery("worker", broker=broker_url, backend="rpc://")


@app.task
def add(x, y):
    return x + y


@app.task
def gpt_answer(question):
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
            Imagine you are {character_name},
            a wise and experienced advisor. Given the context: "{context}",
            how would you respond to this inquiry: "{question}"?',
            1줄로 말해
            (in korean)
            """,
    )

    def generate_prompt(character_name, question, context):
        return prompt_template.format(
            character_name=character_name, question=question, context=context
        )

    character_name = "오은영"
    context = ""

    prompt = generate_prompt(character_name, question, context)

    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
    )

    print(completion.choices[0].message.content)

    return completion.choices[0].message.content


@app.task
def generate_audio_from_string(string, voice_id):
    # edge-tts를 사용하여 텍스트를 음성으로 변환
    async def text_to_speech(text, output_file):
        tts = edge_tts.Communicate(text, voice=voice_id)
        await tts.save(output_file)

    asyncio.run(text_to_speech(string, "input.mp3"))

    # mp3를 wav로 변환 (librosa를 사용하여 처리하기 위해)
    if os.path.exists("input.mp3"):
        y, sr = librosa.load("input.mp3", sr=None)
        buffer = io.BytesIO()
        sf.write(buffer, y, sr, format="WAV")
        buffer.seek(0)

        # 높낮이 조정 (주파수 변경 없이)
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=2)

        # 변환된 오디오 저장
        shifted_buffer = io.BytesIO()
        sf.write(shifted_buffer, y_shifted, sr, format="WAV")
        shifted_buffer.seek(0)

        # 주파수 조정
        samplerate, data = wavfile.read(shifted_buffer)
        new_samplerate = 32000
        number_of_samples = round(len(data) * float(new_samplerate) / samplerate)
        data_resampled = resample(data, number_of_samples)
        resampled_buffer = io.BytesIO()
        wavfile.write(
            resampled_buffer, new_samplerate, data_resampled.astype(data.dtype)
        )
        resampled_buffer.seek(0)

        # SoX를 사용하여 속도 변경 및 로봇 효과 적용
        final_buffer = io.BytesIO()
        with open("temp_resampled.wav", "wb") as f:
            f.write(resampled_buffer.read())
        subprocess.call(
            [
                "sox",
                "temp_resampled.wav",
                "temp_final.wav",
                "tempo",
                "3",
                "pitch",
                "-100",
            ]
        )
        with open("temp_final.wav", "rb") as f:
            final_buffer.write(f.read())
        final_buffer.seek(0)

        # Pydub를 사용하여 mp3로 변환 및 메모리 버퍼에 저장
        audio = AudioSegment.from_wav(final_buffer)
        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format="mp3")
        mp3_buffer.seek(0)

        # Base64로 인코딩
        audio_base64 = base64.b64encode(mp3_buffer.read()).decode("utf-8")

        # 임시 파일 정리
        os.remove("input.mp3")
        os.remove("temp_resampled.wav")
        os.remove("temp_final.wav")

        return audio_base64
    else:
        print(
            "The audio file was not created. Please check the TTS conversion process."
        )
        return None
