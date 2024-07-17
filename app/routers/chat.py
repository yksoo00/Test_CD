from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chat as ChatService
from crud import chatroom as ChatroomService
from crud import prescription as PrescriptionService
from database import get_db
from starlette.websockets import WebSocketDisconnect
from openai import OpenAI
from langchain.memory import ConversationBufferMemory
from utils import opensearch as opensearchService
from utils import celery_worker
import os
import re


router = APIRouter()

GPT_MODEL = "gpt-3.5-turbo"


def load_history_to_memory(chat_history, memory):
    if chat_history:
        memory.chat_memory.messages.extend(chat_history)


def generate_gpt_payload(chat_memory_messages, prompt):
    gpt_payload = [
        {"role": msg["role"], "content": msg["content"]} for msg in chat_memory_messages
    ]
    gpt_payload += [{"role": "assistant", "content": prompt}]
    return gpt_payload


@router.websocket("/chatrooms/{chatroom_id}")
async def websocket_endpoint(
    websocket: WebSocket, chatroom_id: int, user_id: int, db: Session = Depends(get_db)
):
    await websocket.accept()
    chatroom = ChatroomService.get_chatroom(db, chatroom_id=chatroom_id)

    if chatroom is None:
        await websocket.send_json(
            {"event": "disconnect", "message": "Chatroom not found"}
        )
        await websocket.close()
        return

    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        await websocket.send_json({"event": "disconnect", "message": "User not found"})
        await websocket.close()
        return

    await websocket.send_json(
        {
            "event": "connect",
            "message": "connected",
            "user_id": user_id,
            "chatroom_id": chatroom_id,
            "mentor_id": chatroom.mentor_id,
        }
    )

    chat_history = ""
    memory = ConversationBufferMemory()
    try:
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )
        while True:
            client_message = await websocket.receive_text()

            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=True, content=client_message
            )

            memory.chat_memory.messages = []

            load_history_to_memory(chat_history, memory)

            prompt = opensearchService.combined_contexts(
                client_message, chatroom.mentor_id
            )

            gpt_payload = generate_gpt_payload(memory.chat_memory_message, prompt)

            print(gpt_payload)

            gpt_response = client.chat.completions.create(
                model=GPT_MODEL, messages=gpt_payload
            )
            gpt_answer = gpt_response.choices[0].message.content.strip()

            memory.chat_memory.messages.append(
                {"role": "user", "content": client_message}
            )
            memory.chat_memory.messages.append(
                {"role": "assistant", "content": gpt_answer}
            )

            chat_history = memory.buffer_as_messages

            # 음성을 생성하는 celery task 실행
            task_audio = celery_worker.generate_audio_from_string.delay(
                # 한글, 영어, 숫자, 공백만 남기고 제거
                re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9 ]", "", gpt_answer)
            )

            server_audio = task_audio.get()
            await websocket.send_json(
                {
                    "event": "server_message",
                    "message": gpt_answer,
                    "audio": server_audio,
                }
            )

            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=False, content=gpt_answer
            )

    except WebSocketDisconnect:
        prescription = ChatService.get_all_chat(db, chatroom_id=chatroom_id)
        PrescriptionService.create_prescription(
            db,
            user_id=user_id,
            mentor_id=chatroom.mentor_id,
            content=prescription,
        )
        ChatroomService.delete_chatroom(db, chatroom_id=chatroom_id)

        print("client left")
