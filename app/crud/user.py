from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserModify
import logging

logger = logging.getLogger(__name__)


# 사용자 인스턴스 생성 후 DB에 추가해주는 함수
def create_user(db: Session, user: UserCreate):
    logger.debug("User being Created: nickname=%s", user.nickname)
    db_user = User(nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info("User Created: user_id=%d", db_user.id)
    return db_user


# DB에서 유저 불러오는 함수
def get_user(db: Session, user_id: int):
    logger.debug("User being Searched: user_id=%d", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.info("User Not Found: user_id=%d", user_id)
    else:
        logger.info("User Found: user_id=%d", user_id)
    return user


# DB에서 유저 nickname 수정하는 함수
def modify_user(db: Session, user_id: int, user: UserModify):
    logger.debug(
        "User being Modified: user_id=%d, new_nickname=%s", user_id, user.nickname
    )
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        logger.info("User Not Found: user_id=%d", user_id)
        return None
    db_user.nickname = user.nickname
    db.commit()
    db.refresh(db_user)
    logger.info("User Modified: user_id=%d, new_nickname=%s", user_id, user.nickname)
    return db_user
