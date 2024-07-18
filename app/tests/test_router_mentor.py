import unittest
from unittest.mock import patch
from schemas import MentorCreate
from routers import mentor
from models import Mentor
from datetime import datetime


class TestMentorRouter(unittest.TestCase):

    # create_mentor 함수 테스트
    def test_create_mentor(self):
        # given
        test_id = 1
        test_name = "test_name"
        test_description = "test_description"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        new_mentor = MentorCreate(name=test_name, description=test_description)

        with patch(
            "crud.mentor.create_mentor",
            return_value=Mentor(
                id=test_id,
                name=test_name,
                description=test_description,
                created_at=test_created_at,
                updated_at=test_updated_at,
            ),
        ):
            # when
            result = mentor.create_mentor(None, new_mentor)

        # then
        assert result.id == test_id
        assert result.name == test_name
        assert result.description == test_description
        assert result.created_at == test_created_at
        assert result.updated_at == test_updated_at

    # read_mentors 함수 테스트
    def test_read_mentors(self):
        # given
        test_id = 1
        test_name = "test_name"
        test_description = "test_description"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        with patch(
            "crud.mentor.get_mentor_all",
            return_value=[
                Mentor(
                    id=test_id,
                    name=test_name,
                    description=test_description,
                    created_at=test_created_at,
                    updated_at=test_updated_at,
                )
            ],
        ):
            # when
            result = mentor.read_mentors(None)

        # then
        assert len(result) == 1
        assert result[0].id == test_id
        assert result[0].name == test_name
        assert result[0].description == test_description
        assert result[0].created_at == test_created_at
        assert result[0].updated_at == test_updated_at
