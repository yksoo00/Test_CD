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

    history_message = ""
    memory = ConversationBufferMemory()
    try:
        while True:
            client_message = await websocket.receive_text()

            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=True, content=client_message
            )

            memory.chat_memory.messages = []

            ChatService.load_memory(history_message, memory)

            prompt, total_tokens = opensearchService.combined_contexts(
                client_message, chatroom.mentor_id
            )

            memory.chat_memory.messages.append(
                {"role": "user", "content": client_message}
            )

            client = OpenAI(
                api_key=os.environ["OPENAI_API_KEY"],
            )

            messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in memory.chat_memory.messages
            ]
            messages += [{"role": "system", "content": prompt}]

            response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages
            )
            server_message = response.choices[0].message.content.strip()

            memory.chat_memory.messages.append(
                {"role": "assistant", "content": server_message}
            )

            history_message = memory.buffer_as_messages

            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=False, content=server_message
            )
            server_message = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", server_message)

            task_audio = celery_worker.generate_audio_from_string.delay(server_message)

            server_audio = task_audio.get()
            print(f"Total tokens: {total_tokens}")
            await websocket.send_json(
                {
                    "event": "server_message",
                    "message": server_message,
                    "audio": server_audio,
                }
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
