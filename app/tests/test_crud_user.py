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

    def test_get_user(self):
        test_nickname = "test"
        test_user = User(nickname=test_nickname)
        self.db.add(test_user)
        self.db.commit()
        self.db.refresh(test_user)

        db_user = get_user(self.db, test_user.id)
        assert db_user.nickname == test_nickname

    def test_modify_user(self):
        test_nickname = "test"
        test_user = User(nickname=test_nickname)
        self.db.add(test_user)
        self.db.commit()
        self.db.refresh(test_user)

        new_nickname = "new_test"
        modify_user(self.db, test_user.id, UserModify(nickname=new_nickname))

        db_user = self.db.query(User).filter(User.id == test_user.id).first()

        assert db_user.nickname == new_nickname

    def test_modify_user_not_found(self):

        new_nickname = "new_test"
        db_user = modify_user(self.db, 1, UserModify(nickname=new_nickname))

        assert db_user is None
