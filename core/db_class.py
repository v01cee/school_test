from core.repositories import UserRepository
from sqlalchemy.orm import Session

from core.repositories.test_attempt import TestResultRepository


class DBClass:

    def __init__(self, session: Session):
        self.user = UserRepository(session=session)
        self.test_result = TestResultRepository(session)