from sqlalchemy.orm import Session
from models import Mentor
from schemas import MentorCreate


def create_mentor(db: Session, mentor: MentorCreate):
    db_mentor = Mentor(
        name=mentor.name, description=mentor.description, is_spicy=mentor.is_spicy
    )
    db.add(db_mentor)
    db.commit()
    db.refresh(db_mentor)
    return db_mentor
