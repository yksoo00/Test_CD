import unittest
from test_base import SessionLocal, clear_db
from crud.mentor import *


class TestMentor(unittest.TestCase):

    # 테스트 시작 전에 실행
    def setUp(self):
        # 세션 생성
        self.db = SessionLocal()

    # 테스트 종료 후에 실행
    def tearDown(self):
        # DB 초기화
        clear_db()
        # 세션 종료
        self.db.close()

    def test_create_mentor(self):
        test_name = "test_name"
        test_description = "test_description"
        test_mentor = create_mentor(
            self.db, MentorCreate(name=test_name, description=test_description)
        )

        db_mentor = self.db.query(Mentor).filter(Mentor.id == test_mentor.id).first()

        assert db_mentor.name == test_name
        assert db_mentor.description == test_description

    def test_get_mentor(self):
        test_name = "test_name"
        test_description = "test_description"
        test_mentor = Mentor(name=test_name, description=test_description)
        self.db.add(test_mentor)
        self.db.commit()
        self.db.refresh(test_mentor)

        db_mentor = get_mentor(self.db, test_mentor.id)

        assert db_mentor.name == test_name
        assert db_mentor.description == test_description

    def test_get_mentor_all(self):
        test_name = "test_name"
        test_description = "test_description"
        test_mentor = Mentor(name=test_name, description=test_description)
        self.db.add(test_mentor)
        self.db.commit()
        self.db.refresh(test_mentor)

        db_mentors = get_mentor_all(self.db)

        assert len(db_mentors) == 1
        assert db_mentors[0].name == test_name
        assert db_mentors[0].description == test_description
