from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject

from core.db_class import DBClass
from core.keyboard_class import Keyboards
from middlewares.enums import Variables


class BasicMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, db: DBClass):
        self.bot = bot
        self.db = db
        self.keyboards = Keyboards()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        data["variables"] = Variables(
            bot=self.bot,
            db=self.db,
            keyboards=self.keyboards
        )

        callback_query = event.callback_query
        message = event.message
        # print(message)
        if callback_query:
            print(callback_query.data)
        elif message:
            user_id = message.from_user.id
            user = self.db.user.get(user_id=user_id)

            if not user:
                user_data = message.from_user
                self.db.user.add(
                    user_id=user_id,
                    username=user_data.username
                )
        return await handler(event, data)
