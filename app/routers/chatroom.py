from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chatroom as ChatroomService
from crud import mentor as MentorService
from crud import prescription as PrescriptionService
from schemas import *
from database import get_db


router = APIRouter()


# 새로운 채팅방을 생성하는 API
@router.post(" ", response_model=ChatroomResponse)
def create_chatroom(chatroom: ChatroomCreate, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=chatroom.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    mentor = MentorService.get_mentor(db, mentor_id=chatroom.mentor_id)
    if mentor is None:
        raise HTTPException(status_code=404, detail="Mentor not found")

    return ChatroomService.create_chatroom(db=db, chatroom=chatroom)


# 채팅방 목록을 조회하는 API
@router.delete("/{chatroom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chatroom(chatroom_id: int, db: Session = Depends(get_db)):
    chatroom = ChatroomService.get_chatroom(db, chatroom_id)
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    # 처방전 생성
    PrescriptionService.create_prescription(
        db=db,
        chatroom_id=chatroom.id,
        user_id=chatroom.user.id,
        mentor_id=chatroom.mentor.id,
    )

    # 채팅방 삭제
    ChatroomService.delete_chatroom(db, chatroom_id)
