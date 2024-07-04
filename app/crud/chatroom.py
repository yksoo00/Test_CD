from sqlalchemy.orm import Session
from models import *
from schemas import *

def create_chatroom(db: Session, chatroom: ChatroomCreate):
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
    return db_chatroom
