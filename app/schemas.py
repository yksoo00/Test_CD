from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    nickname: str


class UserCreate(UserBase):
    pass


class UserModify(UserBase):
    pass


class UserResponse(UserBase):
    id: int
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


class ChatCreate(BaseModel):
    is_user: bool
    content: str


class MentorBase(BaseModel):
    name: str
    description: str


class MentorCreate(MentorBase):
    pass


class MentorResponse(MentorBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class PrescriptionResponse(BaseModel):
    id: int
    user_id: int
    mentor_id: int
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
