import pytest
from database import clear_db

@pytest.fixture(scope="function", autouse=True)
def clear_tests():
    yield
    clear_db()

def test_create_chatroom(client, user_id, mentor_id):
    chatroom_data = {
        "user_id": user_id,
        "mentor_id": mentor_id,
    }
    response = client.post(
        "/api/chatrooms",
        json=chatroom_data,
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["user_id"] == user_id
    assert response.json()["mentor_id"] == mentor_id

def test_create_chatroom_user_not_found(client, mentor_id):
    chatroom_data = {
        "user_id": 1,
        "mentor_id": mentor_id,
    }
    response = client.post(
        "/api/chatrooms",
        json=chatroom_data,
    )
    assert response.status_code == 404

def test_create_chatroom_mentor_not_found(client, user_id):
    chatroom_data = {
        "user_id": user_id,
        "mentor_id": 1,
    }
    response = client.post(
        "/api/chatrooms",
        json=chatroom_data,
    )
    assert response.status_code == 404