import sys, os

sys.path.append("app/")
os.environ["TESTING"] = "True"

from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database import get_db
from main import app
from database import Base, engine
from models import *
import pytest


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def user_id(client):
    response = client.post(
        "/api/users",
        json={"nickname": "test_nickname"},
    )
    return response.json()["id"]

@pytest.fixture(scope="function")
def mentor_id(client):
    response = client.post(
        "/api/mentors",
        json={"name": "test_mentor", "description": "test mentor description"},
    )
    return response.json()["id"]


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db