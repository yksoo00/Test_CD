from sqlalchemy.orm import Session
from models import *
from schemas import *


def create_user(db: Session, user: UserCreate):
    db_user = User(nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def modify_user(db: Session, user_id: int, user: UserModify):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    db_user.nickname = user.nickname
    db.commit()
    db.refresh(db_user)
    return db_user