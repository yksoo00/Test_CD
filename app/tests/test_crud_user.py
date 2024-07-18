import unittest
from test_base import SessionLocal, clear_db
from crud.user import *


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

    # create_user 함수 테스트
    def test_create_user(self):
        # given
        test_nickname = "test"

        # when
        test_user = create_user(self.db, UserCreate(nickname=test_nickname))

        # then
        db_user = self.db.query(User).filter(User.id == test_user.id).first()
        assert db_user.nickname == test_nickname

    # get_user 함수 테스트
    def test_get_user(self):
        # given
        test_nickname = "test"
        test_user = User(nickname=test_nickname)
        self.db.add(test_user)
        self.db.commit()
        self.db.refresh(test_user)

        # when
        db_user = get_user(self.db, test_user.id)

        # then
        assert db_user.nickname == test_nickname

    # modify_user 함수 테스트
    def test_modify_user(self):
        # given
        test_nickname = "test"
        test_user = User(nickname=test_nickname)
        self.db.add(test_user)
        self.db.commit()
        self.db.refresh(test_user)

        # when
        new_nickname = "new_test"
        modify_user(self.db, test_user.id, UserModify(nickname=new_nickname))

        # then
        db_user = self.db.query(User).filter(User.id == test_user.id).first()
        assert db_user.nickname == "new_test"

    # modify_user 함수 테스트 (유저가 없을 때)
    def test_modify_user_not_found(self):
        # given
        # when
        new_nickname = "new_test"
        db_user = modify_user(self.db, 1, UserModify(nickname=new_nickname))

        # then
        assert db_user is None
