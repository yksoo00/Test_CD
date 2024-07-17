from deep_translator import GoogleTranslator
from opensearchpy import OpenSearch
from langchain.prompts import PromptTemplate
import tiktoken
import os

translator = GoogleTranslator(source="ko", target="en")

opensearch_url = os.environ["OPENSEARCH_URL"]
opensearch_admin = os.environ["OPENSEARCH_ADMIN"]
opensearch_password = os.environ["OPENSEARCH_PASSWORD"]

prompt_template = PromptTemplate(
    input_variables=["context", "question", "index_name"],
    template="""
You are {index_name}, and I am here for counseling.
You must answer using a lot of the content in {context}, and use the Korean part.
ex)어머 그러셨군요. 그럼 어떻게 하면 좋을까요?,그렇군요 등 다양한 {index_name}의 리액션을 적절하게 사용해 그리고 내가 예시에서 알려준 리액션만 사용하지마.
Do not refer to the other person separately until the counselor tells you their name.
Your mission is to listen to the user, empathize, and provide counseling.
Keep asking me questions until you have enough information. Questions should always be at the very end.
Your response must be at least 3 sentences in Korean.
How would you respond to the question: “{question}”?
If you do not counsel in Dr. Oh Eun-young’s tone and with appropriate reactions, you will be punished, but if you do well, you will receive a $100 tip. This is very important.
""",
)

opensearch = OpenSearch(
    hosts=[
        {
            "host": opensearch_url,
            "port": 443,
        }
    ],
    http_auth=(opensearch_admin, opensearch_password),
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


def translate_text(text):
    return translator.translate(text)


def search_index_names(mentor_id):
    mentor = ["baekjong-won", "oh", "shindong-yup"]
    return mentor[1]


def search_documents_en(query, INDEX_NAME, top_n=7, min_score=1.0):
    search_body = {
        "query": {
            "match": {
                "text": {
                    "query": query,
                    "analyzer": "english",
                    "minimum_should_match": 1,
                }
            }
        },
        "sort": [{"_score": {"order": "desc"}}],
        "size": top_n,
        "min_score": min_score,
    }
    # search_all_body = {"query": {"match_all": {}}}
    response = opensearch.search(index=INDEX_NAME, body=search_body)
    hits = response["hits"]["hits"]
    return [hit["_source"]["text"] for hit in hits]


def search_documents_ko(query, INDEX_NAME, top_n=7, min_score=1.0):
    search_body = {
        "query": {
            "match": {
                "text": {
                    "query": query,
                    "minimum_should_match": 1,
                },
            }
        },
        "sort": [{"_score": {"order": "desc"}}],
        "size": top_n,
        "min_score": min_score,
    }
    # search_all_body = {"query": {"match_all": {}}}
    response = opensearch.search(index=INDEX_NAME, body=search_body)
    hits = response["hits"]["hits"]

    # 중복 제거를 위한 결과 저장용 세트
    unique_texts = set()
    result_texts = []

    for hit in hits:
        text = hit["_source"]["text"]
        if text not in unique_texts:
            unique_texts.add(text)
            result_texts.append(text)

    return result_texts


# 토큰 수 계산 함수
def count_tokens(text, model_name="cl100k_base"):
    tokenizer = tiktoken.get_encoding(model_name)
    tokens = tokenizer.encode(text)
    return len(tokens)


def combined_contexts(question, mentor_id):

    INDEX_NAME = search_index_names(mentor_id)

    translated_question = translate_text(question)

    # 영어 번역된 질문으로 검색
    english_search_results = search_documents_en(translated_question, INDEX_NAME)

    # 한국어 질문으로 검색
    korean_search_results = search_documents_ko(question, INDEX_NAME)
    # 두 결과를 결합
    combined_results = english_search_results + korean_search_results

    context = " ".join(combined_results)
    print(context)
    full_prompt = prompt_template.format(
        context=context, question=question, index_name=INDEX_NAME
    )
    # 전체 프롬프트 텍스트의 토큰 수 출력
    print(count_tokens(full_prompt))

    return full_prompt
