from log_config import setup_logging
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic
from routers import chatroom, mentor, user, chat, root, prescription
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.openapi.utils import get_openapi

# 데이터베이스 테이블 생성을 위해 필요
from models import *

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

security = HTTPBasic()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://dw8s2b3nbzq04.cloudfront.net",
    "https://forest-of-thoughts.site",
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


@app.get("/openapi.json", include_in_schema=False)
async def openapi(_: str = Depends(root.get_admin)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


# Instrumentation 설정
Instrumentator().instrument(app).expose(app)
