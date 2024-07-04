from sqlalchemy.orm import Session
from models import *
from schemas import *


def create_mentor(db: Session, mentor: MentorCreate):
    db_mentor = Mentor(
        name=mentor.name, description=mentor.description, is_spicy=mentor.is_spicy
    )
    db.add(db_mentor)
    db.commit()
    db.refresh(db_mentor)
    return db_mentor


def get_mentor(db: Session, mentor_id: int):
    return db.query(Mentor).filter(Mentor.id == mentor_id).first()
