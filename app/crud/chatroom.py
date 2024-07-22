from sqlalchemy.orm import Session
from models import Chatroom
from schemas import ChatroomCreate
import logging

logger = logging.getLogger(__name__)


# 채팅방 인스턴스 생성 후 DB에 추가해주는 함수
def create_chatroom(db: Session, chatroom: ChatroomCreate):
    logger.debug(
        "Chatroom being Created: user_id=%d, mentor_id=%d",
        chatroom.user_id,
        chatroom.mentor_id,
    )
    db_chatroom = Chatroom(user_id=chatroom.user_id, mentor_id=chatroom.mentor_id)
    db.add(db_chatroom)
    db.commit()
    db.refresh(db_chatroom)
    logger.info("Chatroom created: chatroom_id: %d", db_chatroom.id)
    return db_chatroom


# DB에서 채팅방 불러오는 함수
def get_chatroom(db: Session, chatroom_id: int):
    logger.debug("Chatroom being Searched: chatroom_id=%d", chatroom_id)
    db_chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id).first()
    if db_chatroom is None or db_chatroom.is_deleted:
        logger.info("Chatroom Not Found or is_deleted: chatroom_id=%d", chatroom_id)
        return None
    logger.info("Chatroom Found: chatroom_id=%d", chatroom_id)
    return db_chatroom


# DB에서 채팅방 삭제하는 함수
def delete_chatroom(db: Session, chatroom_id: int):
    logger.debug("Chatroom being Deleted: chatroom_id=%d", chatroom_id)
    db_chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id).first()
    if db_chatroom is None:
        logger.info("Chatroom Not Found: chatroom_id=%d", chatroom_id)
        return
    db_chatroom.is_deleted = True
    db.commit()
    logger.info("Chatroom Deleted: chatroom_id=%d", chatroom_id)
