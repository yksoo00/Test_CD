import unittest
from database import SessionLocal, clear_db
from crud.chat import *


class TestChat(unittest.TestCase):

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

    # create_chat 함수 테스트
    def test_create_chat(self):
        # given
        test_is_user = True
        test_chatroom_id = 1
        test_content = "test_content"

        # when
        create_chat(self.db, test_is_user, test_chatroom_id, test_content)

        # then
        db_chat = (
            self.db.query(Chat).filter(Chat.chatroom_id == test_chatroom_id).first()
        )
        assert db_chat.is_user == test_is_user
        assert db_chat.content == test_content

    # get_all_chat 함수 테스트
    def test_get_all_chat(self):
        # given
        test_chatroom_id = 1
        test_content_list = ["test_content1", "test_content2", "test_content3"]

        for test_content in test_content_list:
            test_chat = Chat(
                is_user=True, chatroom_id=test_chatroom_id, content=test_content
            )
            self.db.add(test_chat)
            self.db.commit()
            self.db.refresh(test_chat)

        # when
        chat_list = get_all_chat(self.db, test_chatroom_id)

        # then
        assert chat_list == "\n".join(test_content_list)
