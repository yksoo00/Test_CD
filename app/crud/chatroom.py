from sqlalchemy.orm import Session
from models import Chatroom
from schemas import ChatroomCreate


def create_chatroom(db: Session, chatroom: ChatroomCreate):
    db_chatroom = Chatroom(user_id=chatroom.user_id, mentor_id=chatroom.mentor_id)
    db.add(db_chatroom)
    db.commit()
    db.refresh(db_chatroom)
    return db_chatroom


def get_chatroom(db: Session, chatroom_id: int):
    db_chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id).first()
    if db_chatroom is None or db_chatroom.is_deleted:
        return None
    return db_chatroom


def delete_chatroom(db: Session, chatroom_id: int):
    db_chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id).first()
    db_chatroom.is_deleted = True
    db.commit()
