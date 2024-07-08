from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import user as UserService
from crud import chatroom as ChatroomService
from crud import mentor as MentorService
from crud import prescription as PrescriptionService
from schemas import *
from database import get_db

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/chatrooms/", response_model=ChatroomResponse)
def create_chatroom(chatroom: ChatroomCreate, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=chatroom.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    mentor = MentorService.get_mentor(db, mentor_id=chatroom.mentor_id)
    if mentor is None:
        raise HTTPException(status_code=404, detail="Mentor not found")

    return ChatroomService.create_chatroom(db=db, chatroom=chatroom)


@router.delete("/chatrooms/{chatroom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chatroom(chatroom_id: int, db: Session = Depends(get_db)):
    chatroom = ChatroomService.get_chatroom(db, chatroom_id)
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    # 처방전 생성
    PrescriptionService.create_prescription(
        db=db,
        chatroom_id=chatroom.id,
        user_id=chatroom.user.id,
        mentor_id=chatroom.mentor.id,
    )

    # 채팅방 삭제
    ChatroomService.delete_chatroom(db, chatroom_id)


@router.post("/mentors/", response_model=MentorResponse)
def create_mentor(mentor: MentorCreate, db: Session = Depends(get_db)):
    return MentorService.create_mentor(db=db, mentor=mentor)


@router.get("/mentors/", response_model=list[MentorResponse])
def read_mentors(db: Session = Depends(get_db)):
    mentors = MentorService.get_mentor_all(db)
    return mentors


@router.get("/prescriptions/{prescription_id}", response_model=PrescriptionResponse)
def read_prescription(
    user_id: int, prescription_id: int, db: Session = Depends(get_db)
):
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    prescription = PrescriptionService.get_prescription(db, prescription_id)
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")

    if prescription.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return prescription


@router.get("/prescriptions", response_model=list[PrescriptionResponse])
def read_prescriptions(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    prescriptions = PrescriptionService.get_prescription_all(db, user_id)
    return prescriptions
