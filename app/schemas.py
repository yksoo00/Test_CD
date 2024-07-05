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


class ChatroomCreate(BaseModel):
    user_id: int
    mentor_id: int


class ChatroomResponse(BaseModel):
    id: int
    user_id: int
    mentor_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attribute = True


class MentorBase(BaseModel):
    name: str
    description: str
    is_spicy: bool


class MentorCreate(MentorBase):
    pass


class MentorResponse(MentorBase):
    id: int
    name: str
    is_spicy: bool
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
