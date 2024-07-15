from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserModify


# 사용자 인스턴스 생성 후 DB에 추가해주는 함수
def create_user(db: Session, user: UserCreate):
    db_user = User(nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# DB에서 유저 불러오는 함수
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# DB에서 유저 nickname 수정하는 함수
def modify_user(db: Session, user_id: int, user: UserModify):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    db_user.nickname = user.nickname
    db.commit()
    db.refresh(db_user)
    return db_user
