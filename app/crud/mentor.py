from sqlalchemy.orm import Session
from models import Mentor
from schemas import MentorCreate
import logging

logger = logging.getLogger(__name__)


# 멘토 인스턴스 생성 후 DB에 추가해주는 함수
def create_mentor(db: Session, mentor: MentorCreate):
    logger.debug("Mentor being Created: mentor_name=%s", mentor.name)
    db_mentor = Mentor(name=mentor.name, description=mentor.description)
    db.add(db_mentor)
    db.commit()
    db.refresh(db_mentor)
    logger.info(
        "Mentor created: mentor_id=%d, mentor_name=%s", db_mentor.id, db_mentor.name
    )
    return db_mentor


# DB에서 멘토 불러오는 함수
def get_mentor(db: Session, mentor_id: int):
    logger.debug("Mentor being Searched: mentor_id=%d", mentor_id)
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if mentor is None:
        logger.info("Mentor Not Found: mentor_id=%d", mentor_id)
    else:
        logger.info("Mentor Found: mentor_id=%d", mentor_id)
    return mentor


# DB에서 모든 멘토 불러오는 함수
def get_mentor_all(db: Session):
    logger.debug("Mentor being Searched")
    mentors = db.query(Mentor).all()
    logger.info("Mentor Found: %d mentors", len(mentors))
    return mentors
