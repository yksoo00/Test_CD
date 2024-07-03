import uvicorn
from fastapi import FastAPI
from app.database import Base, engine
from .models import *
from .routers import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
