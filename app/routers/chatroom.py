from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chatroom as ChatroomService
from crud import mentor as MentorService
from schemas import ChatroomCreate, ChatroomResponse
from database import get_db


router = APIRouter()


# 새로운 채팅방을 생성하는 API
@router.post("", response_model=ChatroomResponse, tags=["Chatroom"])
def create_chatroom(chatroom: ChatroomCreate, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=chatroom.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    mentor = MentorService.get_mentor(db, mentor_id=chatroom.mentor_id)
    if mentor is None:
        raise HTTPException(status_code=404, detail="Mentor not found")

    return ChatroomService.create_chatroom(db=db, chatroom=chatroom)
