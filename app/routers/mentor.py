from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import mentor as MentorService
from schemas import MentorCreate, MentorResponse
from database import get_db
import logging

logger = logging.getLogger(__name__)


router = APIRouter()


# 멘토 생성
@router.post("", response_model=MentorResponse, tags=["Mentor"])
def create_mentor(mentor: MentorCreate, db: Session = Depends(get_db)):
    logger.debug("Mentor being Created: mentor_name=%s", mentor.name)
    created_mentor = MentorService.create_mentor(db=db, mentor=mentor)
    logger.info("Mentor Created: mentor_id=%d", created_mentor.id)
    return created_mentor


# 멘토 조회
@router.get("", response_model=list[MentorResponse], tags=["Mentor"])
def read_mentors(db: Session = Depends(get_db)):
    logger.debug("Mentor being Searched")
    mentors = MentorService.get_mentor_all(db)
    mentors_name = [mentor.name for mentor in mentors]
    logger.info("Mentor Searched: mentors=%s", str(mentors_name))
    return mentors


# 디폴트 멘토 생성
@router.post(
    "/create_defaults_mentor", response_model=list[MentorResponse], tags=["Mentor"]
)
def create_default_mentor(db: Session = Depends(get_db)):
    default_mentors = [
        MentorCreate(name="백곰원", description="백종원 설명"),
        MentorCreate(name="오은양", description="오은영 설명"),
        MentorCreate(name="신문엽", description="신동엽 설명"),
    ]
    created_mentors = []
    for default in default_mentors:
        created_mentors.append(MentorService.create_mentor(db=db, mentor=default))
    return created_mentors
