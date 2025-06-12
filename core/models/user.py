from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db_templates.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column()
    full_name: Mapped[str] = mapped_column(nullable=True)
    educational_organization: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    congress: Mapped[bool] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)

    test_attempts = relationship("TestAttempt", back_populates="user")