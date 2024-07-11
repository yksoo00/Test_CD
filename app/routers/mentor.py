from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import mentor as MentorService
from schemas import *
from database import get_db


router = APIRouter()


# 멘토 생성
@router.post("", response_model=MentorResponse, tags=["Mentor"])
def create_mentor(mentor: MentorCreate, db: Session = Depends(get_db)):
    return MentorService.create_mentor(db=db, mentor=mentor)


@router.get("", response_model=list[MentorResponse], tags=["Mentor"])
def read_mentors(db: Session = Depends(get_db)):
    mentors = MentorService.get_mentor_all(db)
    return mentors
