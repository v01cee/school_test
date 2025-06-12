from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from core.db_templates.base_model import BaseModel

class TestAttempt(BaseModel):
    __tablename__ = "test_attempt"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    test_name: Mapped[str]
    correct_answers: Mapped[int]
    total_questions: Mapped[int]
    points: Mapped[int]

    user = relationship("User", back_populates="test_attempts")