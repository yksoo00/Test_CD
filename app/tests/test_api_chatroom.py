import unittest
from conftest import client
from database import clear_db


class TestChatroomApi(unittest.TestCase):

    def tearDown(self):
        clear_db()

    def test_create_user(self):
        test_nickname = "test_nickname"
        response = client.post(
            "/api/users",
            json={"nickname": test_nickname},
        )
        self.user_id = response.json()["id"]

    def test_create_mentor(self):
        test_mentor_name = "test_mentor"
        response = client.post(
            "/api/mentors",
            json={"name": test_mentor_name, "description": "test mentor description"},
        )
        self.mentor_id = response.json()["id"]

    def test_create_chatroom(self):
        self.test_create_user()
        self.test_create_mentor()
    
        chatroom_data = {
            "user_id": self.user_id,
            "mentor_id": self.mentor_id,
        }
        response = client.post(
            "/api/chatrooms",
            json=chatroom_data,
        )
        assert response.status_code == 200
        assert "id" in response.json()
        assert response.json()["user_id"] == self.user_id
        assert response.json()["mentor_id"] == self.mentor_id

    def test_create_chatroom_user_not_found(self):
        self.test_create_mentor()
        mentor_id = self.mentor_id

        chatroom_data = {
            "user_id": 100,
            "mentor_id": mentor_id,
        }

        response = client.post(
            "/api/chatrooms",
            json=chatroom_data,
        )
        assert response.status_code == 404

    def test_create_chatroom_mentor_not_found(self):
        self.test_create_user()
        user_id = self.user_id

        chatroom_data = {
            "user_id": user_id,
            "mentor_id": 100,
        }

        response = client.post(
            "/api/chatrooms",
            json=chatroom_data,
        )
        assert response.status_code == 404
    
