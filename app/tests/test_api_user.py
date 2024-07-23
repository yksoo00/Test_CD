import unittest

from conftest import client
from database import clear_db


class TestUserApi(unittest.TestCase):

    def tearDown(self):
        clear_db()

    def test_create_user(self):
        test_nickname = "test_nickname"
        response = client.post(
            "/api/users",
            json={"nickname": test_nickname},
        )
        assert response.status_code == 200
        assert response.json()["nickname"] == test_nickname

    def test_read_user(self):
        test_nickname = "test_nickname"
        response = client.post(
            "/api/users",
            json={"nickname": test_nickname},
        )
        user_id = response.json()["id"]

        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["nickname"] == test_nickname

    def test_read_user_not_found(self):
        test_user_id = 1
        response = client.get(f"/api/users/{test_user_id}")
        assert response.status_code == 404

    def test_modify_user(self):
        test_nickname = "test_nickname"
        response = client.post(
            "/api/users",
            json={"nickname": test_nickname},
        )
        user_id = response.json()["id"]

        new_nickname = "new_nickname"
        response = client.put(
            f"/api/users/{user_id}",
            json={"nickname": new_nickname},
        )
        assert response.status_code == 200
        assert response.json()["nickname"] == new_nickname

    def test_modify_user_not_found(self):
        test_user_id = 1
        response = client.put(
            f"/api/users/{test_user_id}",
            json={"nickname": "new_nickname"},
        )
        assert response.status_code == 404
