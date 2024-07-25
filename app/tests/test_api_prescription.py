import unittest
from conftest import client
from database import clear_db


class TestPrescriptionApi(unittest.TestCase):

    def tearDown(self):
        clear_db()

    def test_create_user(self):
        test_nickname = "test_nickname"
        response = client.post(
            "/users",
            json={"nickname": test_nickname},
        )
        return response.json()["id"]

    def test_create_mentor(self):
        test_mentor_name = "test_mentor"
        response = client.post(
            "/mentors",
            json={"name": test_mentor_name, "description": "test mentor description"},
        )
        return response.json()["id"]

    def test_create_prescription(self):
        user_id = self.test_create_user()
        mentor_id = self.test_create_mentor()

        prescription_data = {
            "user_id": user_id,
            "mentor_id": mentor_id,
            "content": "Test prescription content",
        }
        response = client.post(
            "/prescriptions",
            json=prescription_data,
        )
        assert response.status_code == 200
        assert "id" in response.json()

    def test_read_prescription(self):
        user_id = self.test_create_user()
        mentor_id = self.test_create_mentor()

        prescription_data = {
            "user_id": user_id,
            "mentor_id": mentor_id,
            "content": "Test prescription content",
        }
        response = client.post(
            "/prescriptions",
            json=prescription_data,
        )
        prescription_id = response.json()["id"]
        response = client.get(
            f"/prescriptions/{prescription_id}", params={"user_id": user_id}
        )
        assert response.status_code == 200
        assert response.json()["id"] == prescription_id

    def test_read_prescription_not_found(self):
        user_id = self.test_create_user()

        test_prescription_id = 1

        response = client.get(
            f"/prescriptions/{test_prescription_id}", params={"user_id": user_id}
        )
        assert response.status_code == 404

    def test_read_prescriptions(self):
        user_id = self.test_create_user()
        mentor_id = self.test_create_mentor()
        num_of_prescriptions = 3

        prescription_data = {
            "user_id": user_id,
            "mentor_id": mentor_id,
            "content": "Test prescription content",
        }

        for _ in range(num_of_prescriptions):
            response = client.post("/prescriptions", json=prescription_data)
            assert response.status_code == 200

        response = client.get("/prescriptions", params={"user_id": user_id})

        assert response.status_code == 200
        assert len(response.json()) == num_of_prescriptions
