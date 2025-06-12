from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.utils.get_admin import get_admins
from menu.fsm.menu import MenuStates
from middlewares.enums import Variables

admin_panel_router = Router()


@admin_panel_router.message(F.text == "/settings")
async def cmd_settings(update: Message | CallbackQuery, state: FSMContext, variables: Variables):
    admin_ids = get_admins()
    user_id = update.from_user.id
    if user_id not in admin_ids:
        await update.answer("⚠️ Только админы могут использовать эту команду!")
        return

    keyboard = await variables.keyboards.admin.admin()
    text = "<i>Админ панель</i>"
    if isinstance(update, CallbackQuery):
        await update.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        await update.answer(
            text=text,
            reply_markup=keyboard
        )