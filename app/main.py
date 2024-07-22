from log_config import setup_logging

from fastapi import FastAPI
from routers import chatroom, mentor, user, chat, root, prescription
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# 데이터베이스 테이블 생성을 위해 필요
from models import *

Base.metadata.create_all(bind=engine)

app = FastAPI(
    root_path="/api",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청받은 엔드포인트로 라우터 연결
app.include_router(user.router, prefix="/users")
app.include_router(chat.router, prefix="/ws")
app.include_router(mentor.router, prefix="/mentors")
app.include_router(chatroom.router, prefix="/chatrooms")
app.include_router(prescription.router, prefix="/prescriptions")
app.include_router(root.router, prefix="")
