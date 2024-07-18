import unittest
from unittest.mock import patch
from fastapi import HTTPException
from schemas import ChatroomCreate
from routers import chatroom
from models import User, Mentor, Chatroom
from datetime import datetime


class TestChatroomRouter(unittest.TestCase):

    # create_chatroom 함수 테스트
    def test_create_chatroom(self):
        # given
        test_id = 1
        test_user_id = 1
        test_mentor_id = 1
        test_nickname = "test_nickname"
        test_name = "test_name"
        test_description = "test_description"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        new_chatroom = ChatroomCreate(user_id=test_user_id, mentor_id=test_mentor_id)

        with patch(
            "crud.user.get_user",
            return_value=User(
                id=test_user_id,
                nickname=test_nickname,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ):
            with patch(
                "crud.mentor.get_mentor",
                return_value=Mentor(
                    id=test_mentor_id,
                    name=test_name,
                    description=test_description,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
            ):
                with patch(
                    "crud.chatroom.create_chatroom",
                    return_value=Chatroom(
                        id=test_id,
                        user_id=test_user_id,
                        mentor_id=test_mentor_id,
                        created_at=test_created_at,
                        updated_at=test_updated_at,
                    ),
                ):
                    # when
                    result = chatroom.create_chatroom(db=None, chatroom=new_chatroom)

        # then
        assert result.id == test_id
        assert result.user_id == test_user_id
        assert result.mentor_id == test_mentor_id
        assert result.created_at == test_created_at
        assert result.updated_at == test_updated_at

    # create_chatroom 함수 테스트 (User not found)
    def test_create_chatroom_user_not_found(self):
        # given
        test_user_id = 1
        test_mentor_id = 1

        new_chatroom = ChatroomCreate(user_id=test_user_id, mentor_id=test_mentor_id)

        with patch(
            "crud.user.get_user",
            return_value=None,
        ):
            # when
            with self.assertRaises(HTTPException) as e:
                chatroom.create_chatroom(db=None, chatroom=new_chatroom)

        # then
        assert e.exception.status_code == 404

    # create_chatroom 함수 테스트 (Mentor not found)
    def test_create_chatroom_mentor_not_found(self):
        # given
        test_user_id = 1
        test_mentor_id = 1
        test_nickname = "test_nickname"

        new_chatroom = ChatroomCreate(user_id=test_user_id, mentor_id=test_mentor_id)

        with patch(
            "crud.user.get_user",
            return_value=User(
                id=test_user_id,
                nickname=test_nickname,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ):
            with patch(
                "crud.mentor.get_mentor",
                return_value=None,
            ):
                # when
                with self.assertRaises(HTTPException) as e:
                    chatroom.create_chatroom(db=None, chatroom=new_chatroom)

        # then
        assert e.exception.status_code == 404
