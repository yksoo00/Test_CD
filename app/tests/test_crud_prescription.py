import unittest
from database import SessionLocal, clear_db
from crud.prescription import *


class TestPrescription(unittest.TestCase):

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

    # create_prescription 함수 테스트
    def test_create_prescription(self):
        # given
        test_user_id = 1
        test_mentor_id = 2
        test_content = "content"

        # when
        prescription = create_prescription(
            self.db, test_user_id, test_mentor_id, test_content
        )

        # then
        self.assertEqual(prescription.user_id, test_user_id)
        self.assertEqual(prescription.mentor_id, test_mentor_id)
        self.assertEqual(prescription.content, test_content)

    # get_prescription 함수 테스트
    def test_get_prescription(self):
        # given
        test_user_id = 1
        test_mentor_id = 2
        test_content = "content"

        test_prescription = Prescription(
            user_id=test_user_id, mentor_id=test_mentor_id, content=test_content
        )
        self.db.add(test_prescription)
        self.db.commit()
        self.db.refresh(test_prescription)

        # when
        db_prescription = get_prescription(self.db, test_prescription.id)

        # then
        self.assertEqual(db_prescription.user_id, test_user_id)
        self.assertEqual(db_prescription.mentor_id, test_mentor_id)
        self.assertEqual(db_prescription.content, test_content)

    # get_prescription_all 함수 테스트
    def test_get_prescription_all(self):
        # given
        test_user_id = 1
        test_mentor_id = 2
        test_content = "content"

        test_prescription = Prescription(
            user_id=test_user_id, mentor_id=test_mentor_id, content=test_content
        )
        self.db.add(test_prescription)
        self.db.commit()
        self.db.refresh(test_prescription)

        # when
        db_prescriptions = get_prescription_all(self.db, test_user_id)

        # then
        self.assertEqual(len(db_prescriptions), 1)
        self.assertEqual(db_prescriptions[0].user_id, test_user_id)
        self.assertEqual(db_prescriptions[0].mentor_id, test_mentor_id)
        self.assertEqual(db_prescriptions[0].content, test_content)
