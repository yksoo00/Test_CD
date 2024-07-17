import unittest
import unittest._log
from test_base import SessionLocal, clear_db
from crud.user import *
from sqlalchemy import MetaData


class TestUser(unittest.TestCase):

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

    def test_create_user(self):
        test_nickname = "test"
        test_user = create_user(self.db, UserCreate(nickname=test_nickname))

        db_user = self.db.query(User).filter(User.id == test_user.id).first()

        assert db_user.nickname == test_nickname
