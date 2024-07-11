from fastapi import FastAPI
from database import Base, engine
from routers import router as user_router
from fastapi.middleware.cors import CORSMiddleware

# 데이터베이스 테이블 생성을 위해 필요
from models import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(user_router, prefix="/api")
