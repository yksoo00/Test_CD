from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import prescription as PrescriptionService
from schemas import *
from database import get_db
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

router = APIRouter()


# 처방전 조회
@router.get(
    "/{prescription_id}", response_model=PrescriptionResponse, tags=["Prescription"]
)
def read_prescription(
    user_id: int, prescription_id: int, db: Session = Depends(get_db)
):
    logger.debug(
        "Prescription being Searched: prescription_id=%d, user_id=%d",
        prescription_id,
        user_id,
    )
    user = UserService.get_user(db, user_id=user_id)
    # 사용자 존재 여부 확인
    if user is None:
        logger.info("User Not Found: user_id=%d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    prescription = PrescriptionService.get_prescription(db, prescription_id)
    # 처방전 존재 여부 확인
    if prescription is None:
        logger.info("Prescription Not Found: prescription_id=%d", prescription_id)
        raise HTTPException(status_code=404, detail="Prescription not found")

    # 처방전을 조회하는 사용자와 처방전의 사용자가 동일한지 확인
    if prescription.user_id != user_id:
        logger.info(
            "User Attempt to Access Prescription belongs to Other User: user_id=%d, prescription_id=%d, other_user_id=%d",
            user_id,
            prescription_id,
            prescription.user_id,
        )
        raise HTTPException(status_code=403, detail="Forbidden")
    else:
        logger.info(
            "Prescription Searched: prescription_id=%d, user_id=%d",
            prescription_id,
            user_id,
        )

    return prescription


# 처방전 목록 조회
@router.get("", response_model=list[PrescriptionResponse], tags=["Prescription"])
def read_prescriptions(user_id: int, db: Session = Depends(get_db)):
    logger.debug("All Prescription belongs to user being Searched: user_id=%d", user_id)
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        logger.info("User Not Found: user_id=%d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    prescriptions = PrescriptionService.get_prescription_all(db, user_id)
    logger.info("Prescription for User Searched: user_id=%d", user_id)
    return prescriptions
