import unittest
from conftest import client
from database import clear_db


class TestMentorApi(unittest.TestCase):

    def tearDown(self):
        clear_db()


    def test_read_mentors(self):
        num_of_mentors = 3
        for _ in range(num_of_mentors):
            test_mentor_name = "test_mentor"
            response = client.post(
                "/api/mentors",
                json={"name": test_mentor_name, "description": "test mentor description"},
            )

        response = client.get(f"/api/mentors")
        assert response.status_code == 200
        mentors = response.json()
        assert len(mentors) == num_of_mentors

    def test_read_mentor_not_found(self):
        test_mentor_id = 1
        response = client.get(f"/api/mentors/{test_mentor_id}")
        assert  response.status_code == 404

    