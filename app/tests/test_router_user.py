import unittest
from unittest.mock import patch
from fastapi import HTTPException
from schemas import UserCreate, UserModify
from routers import user
from models import User
from datetime import datetime


class TestUserRouter(unittest.TestCase):

    # create_user 함수 테스트
    def test_create_user(self):
        # given
        test_id = 1
        test_nickname = "test_nickname"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        new_user = UserCreate(nickname=test_nickname)

        with patch(
            "crud.user.create_user",
            return_value=User(
                id=test_id,
                nickname=test_nickname,
                created_at=test_created_at,
                updated_at=test_updated_at,
            ),
        ):
            # when
            result = user.create_user(db=None, user=new_user)

        # then
        assert result.id == test_id
        assert result.nickname == test_nickname
        assert result.created_at == test_created_at
        assert result.updated_at == test_updated_at

    # read_user 함수 테스트
    def test_read_user(self):
        # given
        test_id = 1
        test_nickname = "test_nickname"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        with patch(
            "crud.user.get_user",
            return_value=User(
                id=test_id,
                nickname=test_nickname,
                created_at=test_created_at,
                updated_at=test_updated_at,
            ),
        ):
            # when
            result = user.read_user(db=None, user_id=test_id)

        # then
        assert result.id == test_id
        assert result.nickname == test_nickname
        assert result.created_at == test_created_at
        assert result.updated_at == test_updated_at

    # read_user 함수 테스트 (유저가 없을 때)
    def test_read_user_not_found(self):
        # given
        test_id = 1

        with patch("crud.user.get_user", return_value=None):
            with self.assertRaises(HTTPException) as context:
                # when
                user.read_user(db=None, user_id=test_id)

        # then
        assert context.exception.status_code == 404

    # modify_user 함수 테스트
    def test_modify_user(self):
        # given
        test_id = 1
        test_nickname = "test_nickname"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        modified_user = UserModify(nickname=test_nickname)

        with patch(
            "crud.user.modify_user",
            return_value=User(
                id=test_id,
                nickname=test_nickname,
                created_at=test_created_at,
                updated_at=test_updated_at,
            ),
        ):
            # when
            result = user.modify_user(db=None, user_id=test_id, user=modified_user)

        # then
        assert result.id == test_id
        assert result.nickname == test_nickname
        assert result.created_at == test_created_at
        assert result.updated_at == test_updated_at

    # modify_user 함수 테스트 (유저가 없을 때)
    def test_modify_user_not_found(self):
        # given
        test_id = 1
        test_nickname = "test_nickname"

        modified_user = UserModify(nickname=test_nickname)

        with patch("crud.user.modify_user", return_value=None):
            with self.assertRaises(HTTPException) as context:
                # when
                user.modify_user(db=None, user_id=test_id, user=modified_user)

        # then
        assert context.exception.status_code == 404
