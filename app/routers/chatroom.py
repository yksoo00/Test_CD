from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chatroom as ChatroomService
from crud import mentor as MentorService
from schemas import ChatroomCreate, ChatroomResponse
from database import get_db
import logging

logger = logging.getLogger(__name__)


router = APIRouter()


# 새로운 채팅방을 생성하는 API
@router.post("", response_model=ChatroomResponse, tags=["Chatroom"])
def create_chatroom(chatroom: ChatroomCreate, db: Session = Depends(get_db)):
    logger.debug(
        "Chatroom being Created: user_id=%d, mentor_id=%d",
        chatroom.user_id,
        chatroom.mentor_id,
    )
    user = UserService.get_user(db, user_id=chatroom.user_id)
    if user is None:
        logger.info("User Not Found: user_id=%d", chatroom.user_id)
        raise HTTPException(status_code=404, detail="User not found")

    mentor = MentorService.get_mentor(db, mentor_id=chatroom.mentor_id)
    if mentor is None:
        logger.info("Mentor Not Found: mentor=%d", chatroom.mentor_id)
        raise HTTPException(status_code=404, detail="Mentor not found")

    created_chatroom = ChatroomService.create_chatroom(db=db, chatroom=chatroom)
    logger.info(
        "Chatrom Created: chatroom_id=%d, user_id=%d, mentor_id=%d",
        created_chatroom.id,
        chatroom.user_id,
        chatroom.mentor_id,
    )
    return created_chatroom
