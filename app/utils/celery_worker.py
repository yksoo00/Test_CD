import os
from celery import Celery
from openai import OpenAI
from langchain.prompts import PromptTemplate

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
        max_tokens=50,
    )

    print(completion.choices[0].message.content)

    return completion.choices[0].message.content
