from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chatroom as ChatroomService
from schemas import *
from database import get_db

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/chatrooms/", response_model=ChatroomResponse)
def create_chatroom(chatroom: ChatroomCreate, db: Session = Depends(get_db)):
    return ChatroomService.create_chatroom(db=db, chatroom=chatroom)


@router.delete("/chatrooms/{chatroom_id}", response_model=ChatroomResponse)
def delete_chatroom(chatroom_id: int, db: Session = Depends(get_db)):
    chatroom = ChatroomService.delete_chatroom(db, chatroom_id=chatroom_id)
    if chatroom is None:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    return chatroom
