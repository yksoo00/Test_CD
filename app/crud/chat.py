from sqlalchemy.orm import Session
from models import *
from schemas import *


def create_chat(db: Session, is_user: bool, chatroom_id: int, content: str):
    db_chat = Chat(is_user=is_user, chatroom_id=chatroom_id, content=content)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_all_chat(db: Session, chatroom_id: int):
    # TODO 로직 구현
    # 전체 채팅을 불러와서 사이에 개행문자 삽입 후 문자열 반환
    pass
