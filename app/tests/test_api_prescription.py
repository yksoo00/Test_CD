import pytest
from database import clear_db

@pytest.fixture(scope="function", autouse=True)
def clear_tests():
    yield
    clear_db()


def test_create_prescription(client, user_id, mentor_id):
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

def test_read_prescription(client, user_id, mentor_id):
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

    response = client.get(f"/prescriptions/{prescription_id}", params={"user_id": user_id})
    assert response.status_code == 200
    assert response.json()["id"] == prescription_id

def test_read_prescription_not_found(client, user_id):
    test_prescription_id = 1
    response = client.get(f"/prescriptions/{test_prescription_id}", params={"user_id": user_id})
    assert response.status_code == 404

def test_read_prescriptions(client, user_id, mentor_id):
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
