from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message, InputFile, FSInputFile
# from aiogram.types import InputMediaPhoto
from aiogram.fsm.context import FSMContext

from core.utils.excel import send_test_results_to_group
from menu.fsm.menu import MenuStates
from middlewares.enums import Variables
from core.utils.photo_id import questions_test2, questions_test1
# from core.utils.photo_id import photo_id_test1, photo_id_test2

menu_callback_router = Router()

@menu_callback_router.callback_query(F.data == "choose_test")
async def choose_test(call: CallbackQuery, variables: Variables):
    keyboard = await variables.keyboards.menu.choose_test()
    await call.message.edit_text(
        text="Выберите тест который хотите пройти",
        reply_markup=keyboard
    )

@menu_callback_router.callback_query(F.data.startswith("group_"))
async def choose_group(call: CallbackQuery, variables: Variables):
    number_test = call.data.split("_")[-1]
    if number_test == "one":
        number_test = 1
    else:
        number_test = 2
    keyboard = await variables.keyboards.menu.confirmation(number_test=number_test)
    if number_test == 1:
        await call.message.edit_text(
            text=("Тестирование ДНТ\n"
                  "1 группа - 20 вопросов (ориентирована на школьников и студентов)"),
            reply_markup=keyboard
        )
    else:
        await call.message.edit_text(
            text=("Тестирование ДНТ\n"
                  "2 группа - 20 вопросов (ориентирована на молодых ученых – аспираты, кандидаты наук до 39 лет)"),
            reply_markup=keyboard
        )

@menu_callback_router.callback_query(F.data.startswith("start_test_"))
async def start_test(call: CallbackQuery, state: FSMContext, variables: Variables):
    number_test = int(call.data.split("_")[-1])
    answer_number = 0
    await state.update_data(
        answer_number=answer_number,
        points=0,
        callback_number=0,
        results={}
    )
    if number_test == 1:
        await state.set_state(MenuStates.test1)
        # await call.message.edit_media(
        #     media=InputMediaPhoto(
        #         media=photo_id_test1[answer_number],
        #         caption=questions_test1[0]  # Текст подписи к медиа
        #     )
        # )
        await call.message.edit_text(
            text=questions_test1[0]
        )
    else:
        await state.set_state(MenuStates.test2)
        # await call.message.edit_media(
        #     InputMediaPhoto(
        #         media=photo_id_test2[answer_number],
        #         caption=questions_test2[0])
        # )
        await call.message.edit_text(
            text=questions_test2[0]
        )

@menu_callback_router.callback_query(F.data.startswith("test1_"))
async def test1_question(call: CallbackQuery, bot: Bot, state: FSMContext, variables: Variables):
    state_data = await state.get_data()
    answer_number = state_data["answer_number"]
    callback_number = state_data["callback_number"]
    points = state_data["points"]
    print(answer_number, callback_number, points)
    callback_number += 1
    mode = call.data.split("_")[-1]
    results = state_data["results"]
    if mode == "correct":
        print(answer_number, results)
        if 5 <= answer_number <= 16  or answer_number == 19:
            points += 4
            results[answer_number + 1] = "1"
        elif answer_number == 17 or answer_number == 18:
            points += 5
            results[answer_number + 1] = "1"
        if answer_number == 19:
            keyboard = await variables.keyboards.menu.test_completion()
            await call.message.edit_text(
                text=f"🎉 <b>Поздравляем! Тест завершен!</b>\n\n"
                     f"Теперь вы стали ещё ближе к науке!\n"
                     f"Со всеми инициативами Десятилетия науки и технологий вы можете ознакомиться на сайте\n"
                     f"https://наука.рф\n\n"
                     f"📊 <b>Ваши результаты: {points} баллов из 100</b>\n\n"
                     f"Если у вас есть вопросы, свяжитесь с организаторами.",
                reply_markup=keyboard
            )
            test_data = {
                "test_name": "Тест №1",
                "user_correct_answers": results,  # Правильные ответы
                "total_points": points,

            }
            await send_test_results_to_group(
                bot=bot,
                user_id=call.from_user.id,
                variables=variables,
                **test_data
            )
            return
        answer_number += 1
        await state.update_data(
            answer_number=answer_number,
            points=points,
            callback_number=callback_number,
            results=results
        )

        await call.message.edit_text(
            text=questions_test1[answer_number],
            reply_markup=await variables.keyboards.menu.test1_question(callback_number=callback_number)
        )
    else:
        if answer_number == 19:
            keyboard = await variables.keyboards.menu.test_completion()
            await call.message.edit_text(
                text=f"🎉 <b>Поздравляем! Тест завершен!</b>\n\n"
                     f"Теперь вы стали ещё ближе к науке!\n"
                     f"Со всеми инициативами Десятилетия науки и технологий вы можете ознакомиться на сайте\n"
                     f"https://наука.рф\n\n"
                     f"📊 <b>Ваши результаты: {points} баллов из 100</b>\n\n"
                     f"Если у вас есть вопросы, свяжитесь с организаторами.",
                reply_markup=keyboard
            )
            test_data = {
                "test_name": "Тест №1",
                "user_correct_answers": results,  # Правильные ответы
                "total_points": points
            }
            await send_test_results_to_group(
                bot=bot,
                user_id=call.from_user.id,
                variables=variables,
                **test_data
            )
            return
        answer_number += 1
        await state.update_data(answer_number=answer_number, callback_number=callback_number)

        await call.message.edit_text(
            text=questions_test1[answer_number],
            reply_markup=await variables.keyboards.menu.test1_question(callback_number=callback_number)
        )

@menu_callback_router.callback_query(F.data.startswith("test2_"))
async def test2_question(call: CallbackQuery, bot: Bot, state: FSMContext, variables: Variables):
    state_data = await state.get_data()
    answer_number = state_data["answer_number"]
    print(answer_number)
    callback_number = state_data["callback_number"]
    points = state_data["points"]
    callback_number += 1
    mode = call.data.split("_")[-1]
    results = state_data["results"]
    if mode == "correct":
        if 1 <= answer_number <= 15:
            points += 5
            results[answer_number + 1] = "1"
        elif 16 <= answer_number <= 19:
            points += 5
            results[answer_number + 1] = "1"
        elif answer_number == 19:
            keyboard = await variables.keyboards.menu.test_completion()
            await call.message.edit_text(
                text=f"🎉 <b>Поздравляем! Тест завершен!</b>\n\n"
                     f"Теперь вы стали ещё ближе к науке!\n"
                     f"Со всеми инициативами Десятилетия науки и технологий вы можете ознакомиться на сайте\n"
                     f"https://наука.рф\n\n"
                     f"📊 <b>Ваши результаты: {points} баллов из 100</b>\n\n"
                     f"Если у вас есть вопросы, свяжитесь с организаторами.",
                reply_markup=keyboard
            )
            test_data = {
                "test_name": "Тест №2",
                "user_correct_answers": results,  # Правильные ответы
                "total_points": points
            }
            await send_test_results_to_group(
                bot=bot,
                user_id=call.from_user.id,
                variables=variables,
                **test_data
            )
            return
        answer_number += 1
        await state.update_data(
            answer_number=answer_number,
            points=points,
            callback_number=callback_number,
            results=results
        )

        await call.message.edit_text(
            text=questions_test2[answer_number],
            reply_markup=await variables.keyboards.menu.test2_question(callback_number=callback_number)
        )
    else:
        if answer_number == 19:
            keyboard = await variables.keyboards.menu.test_completion()
            await call.message.edit_text(
                text=f"🎉 <b>Поздравляем! Тест завершен!</b>\n\n"
                     f"Теперь вы стали ещё ближе к науке!\n"
                     f"Со всеми инициативами Десятилетия науки и технологий вы можете ознакомиться на сайте\n"
                     f"https://наука.рф\n\n"
                     f"📊 <b>Ваши результаты: {points} баллов из 100</b>\n\n"
                     f"Если у вас есть вопросы, свяжитесь с организаторами.",
                reply_markup=keyboard
            )
            test_data = {
                "test_name": "Тест №2",
                "user_correct_answers": results,  # Правильные ответы
                "total_points": points
            }
            await send_test_results_to_group(
                bot=bot,
                user_id=call.from_user.id,
                variables=variables,
                **test_data
            )
            return

        answer_number += 1
        await state.update_data(answer_number=answer_number, callback_number=callback_number)
        await call.message.edit_text(
            text=questions_test2[answer_number],
            reply_markup=await variables.keyboards.menu.test2_question(callback_number=callback_number)
        )

@menu_callback_router.callback_query(F.data.startswith("status_"))
async def status(call: CallbackQuery, state: FSMContext, variables: Variables):
    status = call.data.split("_")[-1]
    if status == "schoolboy":
        status="Школьник"
    elif status == "student":
        status = "Студент"
    else:
        status = "Аспирант/Молодой ученый"

    variables.db.user.update(user_id=call.from_user.id, status=status)
    await state.set_state(MenuStates.educational_organization)
    await call.message.edit_text(
        text="3. Укажите образовательную организацию (полностью)"
    )

@menu_callback_router.callback_query(F.data.startswith("congress_"))
async def congress(call: CallbackQuery, state: FSMContext, variables: Variables):
    mode = call.data.split("_")[-1]
    if mode == "yes":
        congress = True
    else:
        congress = False
    variables.db.user.update(user_id=call.from_user.id, congress=congress)
    await state.set_state(MenuStates.email)
    await call.message.edit_text(
        text="5. Адрес электронной почты"
    )


@menu_callback_router.callback_query(F.data == "give_confirmation")
async def confirmation_handler(call: CallbackQuery, state: FSMContext, variables: Variables):
    # Очищаем состояние
    await state.clear()
    keyboard = await variables.keyboards.menu.menu()
    await call.message.edit_text(
        text="✅ <b>Регистрация прошла успешно!</b>\n\n"
             "Спасибо за согласие на обработку персональных данных.\n"
             "Теперь вы можете пройти тестирование.",
        reply_markup=keyboard
    )