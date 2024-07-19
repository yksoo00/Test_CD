from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect
from langchain.memory import ConversationBufferMemory
from crud import user as UserService
from crud import chat as ChatService
from crud import chatroom as ChatroomService
from crud import prescription as PrescriptionService
from database import get_db
from utils import opensearch as opensearchService
from utils import celery_worker
from utils.gpt import get_gpt_answer
import re
import json


router = APIRouter()


def generate_gpt_payload(client_message, chat_memory_messages, prompt, context):
    # 기존 대화 기록 추가
    gpt_payload = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": client_message},
        {"role": "assistant", "content": context},
    ] + [
        {"role": "assistant", "content": msg["content"]} for msg in chat_memory_messages
    ]

    return gpt_payload


# 문자열을 한글, 영어, 숫자, 공백, 마침표, 쉼표, 물음표만 남기고 제거
def trim_text(text):
    return re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9 .,?]", "", text)


@router.websocket("/chatrooms/{chatroom_id}")
async def websocket_endpoint(
    websocket: WebSocket, chatroom_id: int, user_id: int, db: Session = Depends(get_db)
):
    await websocket.accept()
    chatroom = ChatroomService.get_chatroom(db, chatroom_id=chatroom_id)

    # chatroom이 없을 경우 연결 종료
    if chatroom is None:
        await websocket.send_json(
            {"event": "disconnect", "message": "Chatroom not found"}
        )
        await websocket.close()
        return

    # user_id와 chatroom_id가 일치하지 않을 경우 연결 종료
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        await websocket.send_json({"event": "disconnect", "message": "User not found"})
        await websocket.close()
        return

    # 현재 연결 정보 전송
    await websocket.send_json(
        {
            "event": "connect",
            "message": "connected",
            "user_id": user_id,
            "chatroom_id": chatroom_id,
            "mentor_id": chatroom.mentor_id,
        }
    )

    memory = ConversationBufferMemory()

    try:
        while True:
            client_message = await websocket.receive_text()

            # 사용자의 메시지를 db에 저장
            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=True, content=client_message
            )

            # RAG 모델을 사용하여 prompt 생성
            prompt, context = opensearchService.combined_contexts(
                client_message, chatroom.mentor_id
            )

            # 대화 기록과 prompt를 합쳐서 전달할 payload 생성
            gpt_payload = generate_gpt_payload(
                client_message, memory.chat_memory.messages, prompt, context
            )

            # GPT에게 답변 요청
            gpt_answer = get_gpt_answer(gpt_payload)
            # 대화 기록에 사용자의 메시지와 GPT의 답변 추가
            memory.chat_memory.messages.append(
                {"role": "user", "content": client_message}
            )
            memory.chat_memory.messages.append(
                {"role": "assistant", "content": gpt_answer}
            )

            # 음성을 생성하는 celery task 실행
            server_audio = celery_worker.generate_audio_from_string.delay(
                trim_text(gpt_answer)
            ).get()

            # GPT의 답변과 음성을 클라이언트에게 전송
            await websocket.send_json(
                {
                    "event": "server_message",
                    "message": gpt_answer,
                    "audio": server_audio,
                }
            )

            # GPT의 답변을 db에 저장
            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=False, content=gpt_answer
            )

    # 연결이 끊어졌을 때
    except WebSocketDisconnect:

        prompt = """Create a brief letter-style summary that a counselor sends to a client in Korean based on the following conversation.
The summary should provide a concise solution derived from the conversation.
Limit the length of the summary to no more than a few sentences.
Conversation : """ + json.dumps(
            memory.chat_memory.messages, ensure_ascii=False
        )

        prescription_content = get_gpt_answer(
            [{"role": "assistant", "content": prompt}]
        )

        # 모든 채팅 내용으로 처방전 생성
        PrescriptionService.create_prescription(
            db,
            user_id=user_id,
            mentor_id=chatroom.mentor_id,
            content=prescription_content,
        )

        # 채팅방 삭제
        ChatroomService.delete_chatroom(db, chatroom_id=chatroom_id)


        print("client disconnected")
