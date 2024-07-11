from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chatroom as ChatroomService
from crud import mentor as MentorService
from crud import prescription as PrescriptionService
from schemas import *
from database import get_db
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

router = APIRouter()


# 처방전 조회
@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def read_prescription(
    user_id: int, prescription_id: int, db: Session = Depends(get_db)
):
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    prescription = PrescriptionService.get_prescription(db, prescription_id)
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")

    # 처방전을 조회하는 사용자와 처방전의 사용자가 동일한지 확인
    if prescription.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return prescription


# 처방전 목록 조회
@router.get("", response_model=list[PrescriptionResponse])
def read_prescriptions(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    prescriptions = PrescriptionService.get_prescription_all(db, user_id)
    return prescriptions
