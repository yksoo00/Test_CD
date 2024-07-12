from sqlalchemy.orm import Session
from models import *
from schemas import *


# TODO dummy_content가 아닌 실제 채팅 기록을 삽입하도록 구현
def create_prescription(db: Session, chatroom_id: int, user_id: int, mentor_id: int):
    dummy_content = "dummy content"
    db_prescription = Prescription(
        id=chatroom_id, user_id=user_id, mentor_id=mentor_id, content=dummy_content
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription


def get_prescription(db: Session, prescription_id: int):
    return db.query(Prescription).filter(Prescription.id == prescription_id).first()


def get_prescription_all(db: Session, user_id: int):
    return db.query(Prescription).filter(Prescription.user_id == user_id).all()
