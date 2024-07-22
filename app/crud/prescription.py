from sqlalchemy.orm import Session
from models import Prescription
import logging

logger = logging.getLogger(__name__)


# 처방전 인스턴스 생성 후 DB에 추가해주는 함수
def create_prescription(db: Session, user_id: int, mentor_id: int, content=str):
    logger.debug(
        "Prescription being Created: user_id=%d, mentor_id=%d", user_id, mentor_id
    )
    db_prescription = Prescription(
        user_id=user_id, mentor_id=mentor_id, content=content
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    logger.info("Prescription Created: Prescription_id=%d", db_prescription.id)
    return db_prescription


# DB에서 처방전 불러오는 함수
def get_prescription(db: Session, prescription_id: int):
    logger.debug("Prescription being Searched: prescription_id=%d", prescription_id)
    prescription = (
        db.query(Prescription).filter(Prescription.id == prescription_id).first()
    )
    if prescription is None:
        logger.info("Prescription Not Found: prescription_id=%d", prescription_id)
    else:
        logger.info("Prescription Found: prescription_id=%d", prescription_id)
    return prescription


# DB에서 특정 유저의 모든 불러오는 함수
def get_prescription_all(db: Session, user_id: int):
    logger.debug("All Prescription being Searched: user_id=%d", user_id)
    prescriptions = db.query(Prescription).filter(Prescription.user_id == user_id).all()
    logger.info(
        "Prescription belongs to user_%d Searched: prescriptions=%d",
        user_id,
        len(prescriptions),
    )
    return prescriptions
