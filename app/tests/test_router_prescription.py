import unittest
from unittest.mock import patch
from fastapi import HTTPException
from routers import prescription
from models import User, Prescription
from datetime import datetime


class TestPrescriptionRouter(unittest.TestCase):

    # read_prescription 함수 테스트
    def test_read_prescription(self):
        # given
        test_user_id = 1
        test_mentor_id = 1
        test_prescription_id = 1
        test_user_nickname = "test_nickname"
        test_content = "test_content"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        with patch(
            "crud.user.get_user",
            return_value=User(id=test_user_id, nickname=test_user_nickname),
        ):
            with patch(
                "crud.prescription.get_prescription",
                return_value=Prescription(
                    id=test_prescription_id,
                    user_id=test_user_id,
                    mentor_id=test_mentor_id,
                    content=test_content,
                    created_at=test_created_at,
                    updated_at=test_updated_at,
                ),
            ):
                # when
                result = prescription.read_prescription(
                    user_id=test_user_id,
                    prescription_id=test_prescription_id,
                    db=None,
                )
            assert result.id == test_prescription_id
            assert result.user_id == test_user_id
            assert result.mentor_id == test_mentor_id
            assert result.content == test_content
            assert result.created_at == test_created_at
            assert result.updated_at == test_updated_at

    # read_prescription 함수 테스트 (유저가 없을 때)
    def test_read_prescription_user_not_found(self):
        # given
        test_user_id = 1
        test_prescription_id = 1

        with patch("crud.user.get_user", return_value=None):
            with self.assertRaises(HTTPException) as context:
                # when
                prescription.read_prescription(
                    user_id=test_user_id, prescription_id=test_prescription_id, db=None
                )

        # then
        assert context.exception.status_code == 404

    # read_prescription 함수 테스트 (처방전이 없을 때)
    def test_read_prescription_prescription_not_found(self):
        # given
        test_user_id = 1
        test_user_nickname = "test_nickname"
        test_prescription_id = 1
        with patch(
            "crud.user.get_user",
            return_value=User(id=test_user_id, nickname=test_user_nickname),
        ):
            with patch("crud.prescription.get_prescription", return_value=None):
                with self.assertRaises(HTTPException) as context:
                    # when
                    prescription.read_prescription(
                        user_id=test_user_id,
                        prescription_id=test_prescription_id,
                        db=None,
                    )

        # then
        assert context.exception.status_code == 404

    # read_prescription 함수 테스트 (유저와 처방전의 유저가 다를 때)
    def test_read_prescription_forbidden(self):
        # given
        test_user_id = 1
        test_user_nickname = "test_nickname"
        test_prescription_id = 1
        test_user_id2 = 2
        with patch(
            "crud.user.get_user",
            return_value=User(id=test_user_id, nickname=test_user_nickname),
        ):
            with patch(
                "crud.prescription.get_prescription",
                return_value=Prescription(
                    id=test_prescription_id,
                    user_id=test_user_id2,
                    mentor_id=1,
                    content="test_content",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
            ):
                with self.assertRaises(HTTPException) as context:
                    # when
                    prescription.read_prescription(
                        user_id=test_user_id,
                        prescription_id=test_prescription_id,
                        db=None,
                    )

        # then
        assert context.exception.status_code == 403

    # read_prescriptions 함수 테스트
    def test_read_prescriptions(self):
        # given
        test_user_id = 1
        test_user_nickname = "test_nickname"
        test_prescription_id = 1
        test_mentor_id = 1
        test_content = "test_content"
        test_created_at = datetime.now()
        test_updated_at = datetime.now()

        with patch(
            "crud.user.get_user",
            return_value=User(id=test_user_id, nickname=test_user_nickname),
        ):
            with patch(
                "crud.prescription.get_prescription_all",
                return_value=[
                    Prescription(
                        id=test_prescription_id,
                        user_id=test_user_id,
                        mentor_id=test_mentor_id,
                        content=test_content,
                        created_at=test_created_at,
                        updated_at=test_updated_at,
                    )
                ],
            ):
                # when
                result = prescription.read_prescriptions(user_id=test_user_id, db=None)

            # then
            assert len(result) == 1
            assert result[0].id == test_prescription_id
            assert result[0].user_id == test_user_id
            assert result[0].mentor_id == test_mentor_id
            assert result[0].content == test_content
            assert result[0].created_at == test_created_at
            assert result[0].updated_at == test_updated_at

    # read_prescriptions 함수 테스트 (유저가 없을 때)
    def test_read_prescriptions_user_not_found(self):
        # given
        test_user_id = 1
        with patch("crud.user.get_user", return_value=None):
            with self.assertRaises(HTTPException) as context:
                # when
                prescription.read_prescriptions(user_id=test_user_id, db=None)

        # then
        assert context.exception.status_code == 404
