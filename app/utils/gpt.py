from openai import OpenAI
import os

GPT_MODEL = os.environ["GPT_MODEL"]

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


def get_gpt_answer(gpt_payload):
    gpt_response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=gpt_payload,
        temperature=0.7,
        frequency_penalty=0.2,
    )
    return gpt_response.choices[0].message.content.strip()
