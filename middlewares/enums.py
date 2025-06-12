from aiogram import Bot
from aiogram.client.bot import Bot
from pydantic import BaseModel

from core.db_class import DBClass
from core.keyboard_class import Keyboards


class Variables(BaseModel):
    bot: Bot
    db: DBClass
    keyboards: Keyboards

    class Config:
        arbitrary_types_allowed = True