from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import user as UserService
from schemas import *
from database import get_db


router = APIRouter()


# 새로운 사용자를 생성하는 API
@router.post("", response_model=UserResponse, tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db=db, user=user)


# 사용자 목록을 조회하는 API
@router.get("/{user_id}", response_model=UserResponse, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 사용자 닉네임을 수정하는 API
@router.put("/{user_id}", response_model=UserResponse, tags=["User"])
def modify_user(user_id: int, user: UserModify, db: Session = Depends(get_db)):
    user = UserService.modify_user(db, user_id, user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
