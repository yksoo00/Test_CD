from sqlalchemy.orm import Session
from models import Chat
import logging


logger = logging.getLogger(__name__)


# 채팅 인스턴스 생성 후, DB에 추가해주는 함수
def create_chat(db: Session, is_user: bool, chatroom_id: int, content: str):
    logger.debug(
        "Chat being Created: chatroom_id=%d, content=%s",
        chatroom_id,
        content,
    )
    db_chat = Chat(is_user=is_user, chatroom_id=chatroom_id, content=content)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    logger.info("Chat Created: chat_id=%d", db_chat.id)
    return db_chat


# DB에서 모든 채팅 불러오는 함수
def get_all_chat(db: Session, chatroom_id: int):
    logger.debug("Chat being Searched: chatroom_id=%d", chatroom_id)
    all_chat_list = [
        chat.content
        for chat in db.query(Chat).filter(Chat.chatroom_id == chatroom_id).all()
    ]
    user_chat_list = [
        chat.content
        for chat in db.query(Chat)
        .filter(Chat.chatroom_id == chatroom_id and Chat.is_user == 1)
        .all()
    ]
    server_chat_list = [
        chat.content
        for chat in db.query(Chat)
        .filter(Chat.chatroom_id == chatroom_id and Chat.is_user == 0)
        .all()
    ]
    chat_list_str = "\n".join(all_chat_list)
    logger.info(
        "Chat Found: chatroom_id=%d, user_chats=%d, server_chats=%d",
        chatroom_id,
        len(user_chat_list),
        len(server_chat_list),
    )
    return chat_list_str
