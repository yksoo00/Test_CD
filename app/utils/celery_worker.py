import os
from celery import Celery
from openai import OpenAI
from langchain.prompts import PromptTemplate
from pydub import AudioSegment
from gtts import gTTS
import random
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
def generate_audio_from_string(string, random_factor=0.1):
    result_sound = None
    os.makedirs("samples", exist_ok=True)

    for idx, letter in enumerate(string):
        print(f"Processing letter at index {idx}: '{letter}'")  # 문자 정보 출력
        if letter == " ":
            # 공백 문자 처리 시 기본 값을 사용하여 letter_sound를 정의합니다.
            letter_sound = AudioSegment.silent(duration=50)  # 50ms의 무음 생성
            new_sound = letter_sound._spawn(
                b"\x00" * (44100 // 3), overrides={"frame_rate": 44100}
            )
            new_sound = new_sound.set_frame_rate(44100)
        else:
            sample_path = f"samples/{letter}.mp3"
            if not os.path.isfile(sample_path):
                tts = gTTS(letter, lang="ko")
                tts.save(sample_path)

            letter_sound = AudioSegment.from_mp3(sample_path)
            raw = letter_sound.raw_data[5000:-5000]

            octaves = 2.0 + random.random() * random_factor
            frame_rate = int(letter_sound.frame_rate * (2.0**octaves))
            # print('%s - octaves: %.2f, fr: %d' % (letter, octaves, frame_rate))

            new_sound = letter_sound._spawn(raw, overrides={"frame_rate": frame_rate})
            new_sound = new_sound.set_frame_rate(44100)

        result_sound = new_sound if result_sound is None else result_sound + new_sound

    # 메모리 버퍼에 오디오 데이터 저장
    buffer = io.BytesIO()
    result_sound.export(buffer, format="mp3")
    buffer.seek(0)

    # Base64로 인코딩
    audio_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return audio_base64

