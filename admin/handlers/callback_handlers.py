from io import BytesIO

from aiogram import F, Router, Bot, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InputFile, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from core.utils.excel import send_test_results_to_group
from core.utils.get_excel_admin import export_all_user_results_to_excel
from menu.fsm.menu import MenuStates
from middlewares.enums import Variables
from core.utils.photo_id import photo_id_test1, photo_id_test2, questions_test2, questions_test1

admin_callback_router = Router()

@admin_callback_router.callback_query(F.data == "table_admin")
async def table_admin(call: CallbackQuery, variables: Variables):
    import logging
    logger = logging.getLogger(__name__)
    logger.info("DEBUG: table_admin вызван")
    excel_file: BytesIO = export_all_user_results_to_excel(variables)
    logger.info(f"DEBUG: Excel файл создан, размер: {len(excel_file.getvalue())} bytes")


    document = types.BufferedInputFile(
        file=excel_file.read(),
        filename="user_results.xlsx"
    )


    await call.message.answer_document(
        document=document,
        caption="📊 Общая таблица результатов"
    )


@admin_callback_router.message(Command("reset"))
async def reset_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Ваше состояние очищено.")