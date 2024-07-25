from fastapi.responses import HTMLResponse
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from typing import Annotated
import secrets
from fastapi.openapi.docs import get_swagger_ui_html
import os


# 데이터베이스 테이블 생성을 위해 필요
from models import *


router = APIRouter()

security = HTTPBasic()
ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]


def get_admin(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return ""


@router.get("/")
async def get():
    return HTMLResponse(open("./templates/index.html").read())


@router.get("/docs", include_in_schema=False)
async def get_documentation(admin: str = Depends(get_admin)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
