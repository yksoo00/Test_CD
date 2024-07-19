from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/")
async def get():
    return HTMLResponse(open("./templates/index.html").read())
