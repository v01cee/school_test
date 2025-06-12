from sqlalchemy import insert, select, update, delete

from core.db_templates.base_repository import BaseRepository
from core.models import User


class UserRepository(BaseRepository):

    def add(
            self,
            user_id: int,
            username: str
    ):
        insert_stmt = insert(User).values(
            user_id=user_id,
            username=username
        )
        self.session.execute(statement=insert_stmt)
        self.session.commit()

    def get(
        self,
        user_id: int | None = None,
        every: bool | None = None
    ) -> User | list[User] | None:
        result = None

        if user_id:
            select_stmt = select(User).where(
                User.user_id == user_id
            )
            result = self.session.execute(statement=select_stmt)
            result = result.scalar_one_or_none()

        elif every:
            select_stmt = select(User)
            result = self.session.execute(statement=select_stmt)
            result = result.scalars().all()

        return result

    def update(
            self,
            user_id: int,
            **kwargs
    ):
        update_stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(**kwargs)
        )
        self.session.execute(statement=update_stmt)
        self.session.commit()
