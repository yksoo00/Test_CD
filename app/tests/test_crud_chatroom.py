import unittest
from database import SessionLocal, clear_db
from crud.chatroom import *


class TestChatroom(unittest.TestCase):

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

    # create_chatroom 함수 테스트
    def test_create_chatroom(self):
        # given
        test_user_id = 1
        test_mentor_id = 1

        # when
        test_chatroom = create_chatroom(
            self.db, ChatroomCreate(user_id=test_user_id, mentor_id=test_mentor_id)
        )

        # then
        db_chatroom = (
            self.db.query(Chatroom).filter(Chatroom.id == test_chatroom.id).first()
        )
        assert db_chatroom.user_id == test_user_id
        assert db_chatroom.mentor_id == test_mentor_id

    # get_chatroom 함수 테스트
    def test_get_chatroom(self):
        # given
        test_user_id = 1
        test_mentor_id = 1
        test_chatroom = Chatroom(user_id=test_user_id, mentor_id=test_mentor_id)
        self.db.add(test_chatroom)
        self.db.commit()
        self.db.refresh(test_chatroom)

        # when
        db_chatroom = get_chatroom(self.db, test_chatroom.id)

        # then
        assert db_chatroom.user_id == test_user_id
        assert db_chatroom.mentor_id == test_mentor_id

    # delete_chatroom 함수 테스트
    def test_delete_chatroom(self):
        # given
        test_user_id = 1
        test_mentor_id = 1
        test_chatroom = Chatroom(user_id=test_user_id, mentor_id=test_mentor_id)
        self.db.add(test_chatroom)
        self.db.commit()
        self.db.refresh(test_chatroom)

        # when
        delete_chatroom(self.db, test_chatroom.id)

        # then
        db_chatroom = (
            self.db.query(Chatroom).filter(Chatroom.id == test_chatroom.id).first()
        )
        assert db_chatroom.is_deleted == True
