from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from pyexpat.errors import messages

from menu.fsm.menu import MenuStates
from middlewares.enums import Variables

start_router = Router()


@start_router.callback_query(F.data == "menu")
@start_router.message(F.text == "/start")
async def cmd_start(update: Message | CallbackQuery, state: FSMContext, variables: Variables):
    user = variables.db.user.get(user_id=update.from_user.id)
    keyboard = await variables.keyboards.menu.menu()
    if not user or not user.email:
        await state.set_state(MenuStates.registration)
        await update.answer(
            text="Добро пожаловать! Давайте пройдём регистрацию\n1. Укажите ФИО (полностью)"
        )
        return

    text = "Добро пожаловать!"
    if isinstance(update, CallbackQuery):
        await update.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    else:
        await update.answer(
            text=text,
            reply_markup=keyboard
        )