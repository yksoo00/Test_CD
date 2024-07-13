from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import mentor as MentorService
from schemas import MentorCreate, MentorResponse
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


@router.post(
    "/create_defaults_mentor", response_model=list[MentorResponse], tags=["Mentor"]
)
def create_default_mentor(db: Session = Depends(get_db)):
    default_mentors = [
        MentorCreate(name="오은영", description="오은영 설명"),
        MentorCreate(name="백종원", description="백종원 설명"),
        MentorCreate(name="신동엽", description="신동엽 설명"),
    ]
    created_mentors = []
    for default in default_mentors:
        created_mentors.append(MentorService.create_mentor(db=db, mentor=default))
    return created_mentors
