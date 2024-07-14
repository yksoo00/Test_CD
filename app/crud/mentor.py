from sqlalchemy.orm import Session
from models import Mentor
from schemas import MentorCreate


# 멘토 인스턴스 생성 후 DB에 추가해주는 객체
def create_mentor(db: Session, mentor: MentorCreate):
    db_mentor = Mentor(name=mentor.name, description=mentor.description)
    db.add(db_mentor)
    db.commit()
    db.refresh(db_mentor)
    return db_mentor


# DB에서 멘토 불러오는 객체
def get_mentor(db: Session, mentor_id: int):
    return db.query(Mentor).filter(Mentor.id == mentor_id).first()


# DB에서 모든 멘토 불러오는 객체
def get_mentor_all(db: Session):
    return db.query(Mentor).all()
