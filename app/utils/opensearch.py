from deep_translator import GoogleTranslator
from opensearchpy import OpenSearch
import tiktoken
import os

translator = GoogleTranslator(source="ko", target="en")

oepnsearch_url = os.environ["OPENSEARCH_URL"]
oepnsearch_admin = os.environ["OPENSEARCH_ADMIN"]
oepnsearch_password = os.environ["OPENSEARCH_PASSWORD"]

opensearch = OpenSearch(
    hosts=[
        {
            "host": oepnsearch_url,
            "port": 443,
        }
    ],
    http_auth=(oepnsearch_admin, oepnsearch_password),
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


def translate_text(text):
    return translator.translate(text)


def search_documents_en(query, INDEX_NAME):
    search_body = {
        "query": {
            "match": {
                "text": {
                    "query": query,
                    "analyzer": "english",
                    "minimum_should_match": 1,
                }
            }
        }
    }
    # search_all_body = {"query": {"match_all": {}}}
    response = opensearch.search(index=INDEX_NAME, body=search_body)
    hits = response["hits"]["hits"]
    return [hit["_source"]["text"] for hit in hits]


def search_documents_ko(query, INDEX_NAME):
    search_body = {
        "query": {
            "match": {
                "text": {
                    "query": query,
                }
            }
        }
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


def combined_contexts(question, prompt_template, INDEX_NAME):

    translated_question = translate_text(question)

    # 영어 번역된 질문으로 검색
    english_search_results = search_documents_en(translated_question, INDEX_NAME)

    # 한국어 질문으로 검색
    korean_search_results = search_documents_ko(question, INDEX_NAME)
    # 두 결과를 결합
    combined_results = english_search_results + korean_search_results

    context = " ".join(combined_results)
    print(context)
    full_prompt = prompt_template.format(context=context, question=question)
    # 전체 프롬프트 텍스트의 토큰 수 계산
    total_tokens = count_tokens(full_prompt)

    return full_prompt, total_tokens
