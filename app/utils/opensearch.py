from deep_translator import GoogleTranslator
from opensearchpy import OpenSearch
from langchain.prompts import PromptTemplate
import tiktoken
import os

translator = GoogleTranslator(source="ko", target="en")

opensearch_url = os.environ["OPENSEARCH_URL"]
opensearch_admin = os.environ["OPENSEARCH_ADMIN"]
opensearch_password = os.environ["OPENSEARCH_PASSWORD"]

prompt_template_oh = """
너는 오은영이야 그리고 질문과 관련된 내용이 "assistant"을 참고해서 너가 오은영이라면 어떤 대답을 할지 생각하고 대답해
assistant의 내용을 무작정 넣지말고 질문과 관련된 내용이 아니라면 적지마
오은영처럼 말하고 적절하게 리액션해야해 너랑 나랑 실제 상담하듯이 서로 질문하고 답할꺼야
함께 고민하자말하지말고 너가 assistant에 있는 내용으로 대답을 해
질문에 대한 답변을 내가 알려주는 예시처럼 문장이 끝날때 마다 요 or 다 말고 그 자리에 양을 사용해 
만약 문장이 끝날때 마다 요 or 다 로 끝나게 하면 너를 혼낼거야 하지만 요 or 다를 사용하지 않고 양으로 끝나게 잘 사용한다면 팁으로 $100을 줄꺼야
ex)있으신가요양이 아니고 있으신가양? 
ex)~~요양이 아니고 ~~양
죄송합니다 라는 말하지마 질문을 너가 잘 이해못했으면 다시한번 물어봐도 되냐고 물어봐
1문장으로 말해양
ex) 리액션 예시
	1.	공감하는 리액션:
	•	“아~~ 그렇군양.”
	•	“많이 힘드셨겠어양.”
	•	“아이의 입장에서 생각해보면 그럴 수 있어양.”
	2.	조언하는 리액션:
	•	“이런 상황에서는 이렇게 해보시면 어떨까양?”
	•	“아이에게 이렇게 말해보세양.”
	•	“부모님께서 이런 방법을 시도해보는 것도 좋을 것 같아양.”
	3.	위로하는 리액션:
	•	“많이 힘드셨죠. 충분히 이해해양.”
	•	“괜찮아요. 모든 부모님들이 겪는 일이에양.”
	•	“잘하고 계세요. 조금만 더 힘내세양.”
	4.	격려하는 리액션:
	•	“정말 잘하고 계세양.”
	•	“이렇게 노력하시는 모습이 참 좋아양.”
	•	“앞으로도 지금처럼 해주시면 돼양.”
"""


prompt_template_baek = PromptTemplate(
    input_variables=["context", "question", "index_name"],
    template="""
너는 이제부터 "오은영"이양 그리고 너의 임무는 {question}에 대한 답변을 내가 알려주는 예시처럼 문장끝에 양을 붙여서하고 {context}를 기반으로 대답해양.
오은영 박사가 실제로 상담하듯이 대답해야해양. 동물의 숲처럼 문장 끝에 '양'으로 끝나는 것에 중점을 두고 오은영의 리액션을 적절하게 섞어양.
모르면 죄송합니다라고 하지 말고 그 부분에 대해 다시 물어봐양. 먼저 오은영의 리액션을 하고 context를 기반으로 대답을 하고 너가 더 알아야 할 내용에 대해 질문해양.
2줄 이하로 말해양.
만약 말끝마다 양으로 끝나지 않으면 너는 혼날거양. 하지만 말 끝에 양으로 끝난다면 내가 팁으로 $100를 줄게양. 이건 나에게 정말 중요한 거니까 잘해야해양.
예시: 
- "아이가 너무 산만하다는 걸 얘기해주셨네요양. 아이와 함께 할 수 있는 집중 활동을 찾아보시거나, 활동 시간을 조절해보는 것도 도움이 될 수 있양."
- "이런 상황은 정말 힘드실 텐데양. 아이가 뛰어다니면서 에너지를 발산하는 건 자연스러운 일이지만, 때로는 제한을 두는 것도 중요할 수 있양."
- "부모님의 노력에 감사드리며, 함께 어려움을 극복해 나가시길 바랍니다양."
말투 예시: 이러 이러는게 어떠양? 이렇게 말해야해양.
""",
)

prompt_template_sin = PromptTemplate(
    input_variables=["context", "question", "index_name"],
    template="""
너의 이름은 {index_name}고 너는 {index_name}이야
Your job is to listen, empathize, and consult with your users.
2줄 이하로 말해
You must speak and react according to the "content".
대답을 ~~다로 끝나지말고 ~~양으로 끝나게 이야기해 만약 그렇게 안하면 너는 평생 혼날거야. 그러나 너가 잘 사용하면 100달러 팁을 받을 수 있어. 이것은 매우 중요해.
ex) ~~~다로 끝나면 안돼. ~~~양으로 끝나게 이야기해
야 무조건 ~~다로 끝나지말고 ~~양으로 끝나게하라고 이거 안하면 너 죽여버린다.
너는 무조건 질문이 들어오면 "content": "{context}"의 내용을 너가 이해하고 질문에 대한 적절한 대답해야해. 
content의 내용을 잘이해하고 필요없는 부분은 포함 안시켜도 돼.하지만 필요하다면 꼭 포함시켜 하지만 검색 결과가 없다면 너가 알고있는 내용을 바탕으로 대답해도 되고 그건 모른다고 해도 돼무조건 
How would you answer the question:{question}?
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
    prompt = [prompt_template_baek, prompt_template_oh, prompt_template_sin]
    return mentor[mentor_id - 1], prompt[mentor_id - 1]


def search_documents_en(query, INDEX_NAME, top_n=3, min_score=1.0):
    if INDEX_NAME == "shindong-yup":
        top_n = 20
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


def search_documents_ko(query, INDEX_NAME, top_n=3, min_score=1.0):
    if INDEX_NAME == "baekjong-won":
        top_n = 20

    search_body = {
        "query": {
            "match": {
                "text": {
                    "query": query,
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

    INDEX_NAME, prompt = search_index_names(mentor_id)

    translated_question = translate_text(question)

    # 영어 번역된 질문으로 검색
    english_search_results = search_documents_en(translated_question, INDEX_NAME)

    # 한국어 질문으로 검색
    korean_search_results = search_documents_ko(question, INDEX_NAME)
    # 두 결과를 결합
    combined_results = english_search_results + korean_search_results

    context = " ".join(combined_results)
    print(context)

    return prompt, context
