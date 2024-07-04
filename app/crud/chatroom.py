from sqlalchemy.orm import Session
from models import *
from schemas import *
from fastapi import HTTPException, status

def create_chatroom(db: Session, chatroom: ChatroomCreate):
    user = db.query(User).filter(User.id == chatroom.user_id).first()
    mentor = db.query(Mentor).filter(Mentor.id == chatroom.mentor_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not mentor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found")


    db_chatroom = Chatroom(user_id=chatroom.user_id, mentor_id=chatroom.mentor_id)
    db.add(db_chatroom)
    db.commit()
    db.refresh(db_chatroom)
    return db_chatroom

def delete_chatroom(db: Session, chatroom_id: int):
    db_chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id).first()
    if db_chatroom:
        db_chatroom.is_deleted = True
        db.commit()
        return True
    return False
