from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chat as ChatService
from crud import chatroom as ChatroomService
from crud import prescription as PrescriptionService
from database import get_db
from starlette.websockets import WebSocketDisconnect
from openai import OpenAI
from langchain.prompts import PromptTemplate
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
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
너는 `오은영 박사님`이야, and I am here for counseling.
너는 반드시 context를 기반으로"{context}", `오은영 박사님의 말`투로을 말해 그리고 리액션을 적절히 해야 해.
너의 임무는 실제 상담하듯이 말하는 것이야.
충분한 정보가 생길 때까지 나에게 질문을 해. 질문은 항상 맨 마지막에 넣어야 해.
Your response should be between 2 to 4 sentences.
Context: {context}
How would you respond to the question: "{question}"?
(in Korean)
오은영 박사님 말투와 리액션으로 상담을 하지 않으면 벌을 줄거야 하지만 잘하면 팁으로 100$를 줄게. 이거 매우 중요해.
""",
    )

    context = ""
    history_message = ""
    index_name = "oh"
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
                client_message, prompt_template, index_name
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

            # 음성을 생성하는 celery task 실행
            task_audio = celery_worker.generate_audio_from_string.delay(
                # 한글, 영어, 숫자, 공백만 남기고 제거
                re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9 ]", "", server_message)
            )

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
