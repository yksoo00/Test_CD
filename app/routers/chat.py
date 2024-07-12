from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chat as ChatService
from crud import chatroom as ChatroomService
from schemas import *
from database import get_db
from starlette.websockets import WebSocketDisconnect
from utils import celery_worker

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

    try:
        while True:
            client_message = await websocket.receive_text()
            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=True, content=client_message
            )
            print(f"Client: {client_message}")

            task = celery_worker.gpt_answer.delay(client_message)

            server_message = task.get()
            ChatService.create_chat(
                db, chatroom_id=chatroom_id, is_user=False, content=server_message
            )
            print(f"Server: {server_message}")

            # server_audio_task = generate_audio_from_string.apply_async(
            #     args=[server_message],
            # )

            await websocket.send_json(
                {
                    "event": "server_message",
                    "message": server_message,
                    # "audio": server_audio_task.get(),
                }
            )

    except WebSocketDisconnect:
        print("client left")
