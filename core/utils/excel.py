import pandas as pd
from io import BytesIO
from aiogram import Bot, types
from dotenv import load_dotenv
import os

from middlewares.enums import Variables

# Загружаем переменные из .env
load_dotenv()


async def send_test_results_to_group(
        bot: Bot,
        test_name: str,
        user_correct_answers: dict[int, int],
        total_points: int,
        user_id: int,
        variables: Variables
):
    """Отправляет результаты теста в группу Telegram"""
    # Получаем ID группы из переменных окружения
    group_id = int(os.getenv('TELEGRAM_GROUP_ID'))

    # Создаем DataFrame с 20 вопросами
    total_questions = 20
    total_correct = len(user_correct_answers)

    variables.db.test_result.add(
        user_id=user_id,
        test_name=test_name,
        correct_answers=total_correct,
        total_questions=total_questions,
        points=total_points
    )
    # Основная таблица с вопросами
    df = pd.DataFrame({
        "№ вопроса": range(1, total_questions + 1),
        "Результат": ["✓" if q in user_correct_answers else "✗"
                      for q in range(1, total_questions + 1)]
    })

    # Добавляем служебные строки
    df.loc[-1] = ["Тест", test_name]
    df.loc[-2] = ["ИТОГО", f"{total_correct}/{total_questions}"]
    df.loc[-3] = ["Баллы", str(total_points)]
    df = df.sort_index().reset_index(drop=True)

    # Создаем Excel-файл в памяти
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, sheet_name="Результаты")
    excel_buffer.seek(0)


    # Отправляем в группу
    await bot.send_document(
        chat_id=group_id,
        document=types.BufferedInputFile(
            file=excel_buffer.read(),
            filename=f"Результаты_{test_name.replace(' ', '_')}.xlsx"
        ),
        caption=f"📊 Результаты теста: {test_name}\n"
                f"✅ Правильных ответов: {total_correct}/{total_questions}\n"
                f"🏆 Набрано баллов: {total_points}"
    )
