from sqlalchemy.orm import Session
from models import *
from schemas import *


def create_chat(db: Session, is_user: bool, chatroom_id: int, content: str):
    db_chat = Chat(is_user=is_user, chatroom_id=chatroom_id, content=content)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat
