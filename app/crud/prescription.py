from sqlalchemy.orm import Session
from models import Prescription


# 처방전 인스턴스 생성 후 DB에 추가해주는 객체
def create_prescription(db: Session, user_id: int, mentor_id: int, content=str):
    db_prescription = Prescription(
        user_id=user_id, mentor_id=mentor_id, content=content
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription


# DB에서 처방전 불러오는 객체
def get_prescription(db: Session, prescription_id: int):
    return db.query(Prescription).filter(Prescription.id == prescription_id).first()


# DB에서 특정 유저의 모든 불러오는 객체
def get_prescription_all(db: Session, user_id: int):
    return db.query(Prescription).filter(Prescription.user_id == user_id).all()
