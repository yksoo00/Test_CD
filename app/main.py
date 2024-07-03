import uvicorn
from fastapi import FastAPI
from app.database import Base, engine
from .models import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
