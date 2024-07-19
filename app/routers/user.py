from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import user as UserService
from schemas import UserCreate, UserModify, UserResponse
from database import get_db
import logging


# 로깅 설정
logger = logging.getLogger(__name__)


router = APIRouter()


# 새로운 사용자를 생성하는 API
@router.post("", response_model=UserResponse, tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.debug("Creating user details: %s", user)
    created_user = UserService.created_user(db=db, user=user)
    logger.info("Created user ID : %d", created_user.id)
    return created_user


# 사용자 목록을 조회하는 API
@router.get("/{user_id}", response_model=UserResponse, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    logger.debug("Searching user's user_id: %d", user_id)
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        logger.info("Not found user_id: %d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    else:
        logger.info("Found user_id: %d", user_id)
    return user


# 사용자 닉네임을 수정하는 API
@router.put("/{user_id}", response_model=UserResponse, tags=["User"])
def modify_user(user_id: int, user: UserModify, db: Session = Depends(get_db)):
    logger.debug("User_id: %d nickname modified as: %s", user_id, user)
    user = UserService.modify_user(db, user_id, user)
    if user is None:
        logger.info("Not found user_id: %d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    else:
        logger.info("User_ID: %d modified successfully as %s", user_id, user)
    return user
