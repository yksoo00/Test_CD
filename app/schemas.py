from pydantic import BaseModel
import datetime


class UserCreate(BaseModel):
    nickname: str


class UserResponse(BaseModel):
    id: int
    nickname: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attribute = True
