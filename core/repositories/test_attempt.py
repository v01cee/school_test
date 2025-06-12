# core/repositories/test_result.py

from sqlalchemy import insert, select
from core.db_templates.base_repository import BaseRepository
from core.models import TestAttempt, User


class TestResultRepository(BaseRepository):
    def add(
        self,
        user_id: int,
        test_name: str,
        correct_answers: int,
        total_questions: int,
        points: int
    ):
        insert_stmt = insert(TestAttempt).values(
            user_id=user_id,
            test_name=test_name,
            correct_answers=correct_answers,
            total_questions=total_questions,
            points=points
        )
        self.session.execute(statement=insert_stmt)
        self.session.commit()

    def get_by_user(self, user_id: int) -> list[TestAttempt]:
        select_stmt = select(TestAttempt).where(TestAttempt.user_id == user_id)
        result = self.session.execute(statement=select_stmt)
        return result.scalars().all()

    def get_all(self) -> list[TestAttempt]:
        select_stmt = select(TestAttempt)
        result = self.session.execute(statement=select_stmt)
        return result.scalars().all()

    def get_all_with_users(self) -> list[tuple[TestAttempt, User]]:
        stmt = (
            select(TestAttempt, User)
            .join(User, TestAttempt.user_id == User.user_id)
        )
        result = self.session.execute(stmt).all()
        return result