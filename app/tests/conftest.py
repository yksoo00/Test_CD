import sys, os

sys.path.append("app/")
os.environ["TESTING"] = "True"

from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database import get_db
from main import app
from database import Base, engine
from models import *

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
