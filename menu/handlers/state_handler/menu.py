from gc import callbacks

from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from core.utils.photo_id import photo_id_test1, questions_test1, answers_choices_test1, answers_choices_test2, \
    questions_test2
from menu.fsm.menu import MenuStates
from middlewares.enums import Variables

menu_state_router = Router()

@menu_state_router.message(F.text, StateFilter(MenuStates.test1))
async def test(message: Message, state: FSMContext, variables: Variables):
    state_data = await state.get_data()
    answer_number = state_data["answer_number"]
    points = state_data["points"]
    results = state_data["results"]

    if answer_number <= 3 :

        if message.text.strip().lower().replace("ё", "е") == answers_choices_test1[answer_number]:
            points += 7
            results[answer_number+1] = "1"


        answer_number += 1
        await state.update_data(
            answer_number=answer_number,
            points=points
        )
        await message.answer_photo(
            photo=photo_id_test1[answer_number],
            caption=questions_test1[answer_number]
        )
    elif answer_number == 4:
        answer_number += 1
        result_list = [word.strip() for word in message.text.split(",")]
        if result_list == answers_choices_test1[4]:

            results[answer_number] = "1"

            points += 10

        await state.update_data(
            answer_number=answer_number,
            points=points,
            results=results
        )
        callback_number = state_data["callback_number"]

        keyboard = await variables.keyboards.menu.test1_question(callback_number=callback_number)
        await message.answer(
            text=questions_test1[answer_number],
            reply_markup=keyboard
        )

@menu_state_router.message(F.text, StateFilter(MenuStates.test2))
async def test(message: Message, state: FSMContext, variables: Variables):
    state_data = await state.get_data()
    answer_number = state_data["answer_number"]
    points = state_data["points"]
    results = state_data["results"]
    result_list = [word.strip().replace('ё', 'е') for word in message.text.lower().split(",")]
    if result_list == answers_choices_test1[0]:
        points += 10
        results[answer_number + 1] = "1"
    answer_number += 1
    await state.update_data(
        answer_number=answer_number,
        points=points,
        results=results
    )
    callback_number = state_data["callback_number"]

    keyboard = await variables.keyboards.menu.test2_question(callback_number=callback_number)
    await message.answer(
        text=questions_test2[answer_number],
        reply_markup=keyboard
    )

@menu_state_router.message(StateFilter(MenuStates.registration))
async def registration(message: Message, state: FSMContext, variables: Variables):
    full_name = message.text.strip()

    variables.db.user.update(user_id=message.from_user.id, full_name=full_name)  # или следующий шаг
    await message.answer(
        "2. К какой категории вы относитесь? 1. Школьник 2. Студент 3. Аспирант/Молодой ученый",
        reply_markup=await variables.keyboards.menu.registration_1()
    )


@menu_state_router.message(F.text, StateFilter(MenuStates.educational_organization))
async def educational_organization(message: Message, variables: Variables):
    educational_organization = message.text
    keyboard = await variables.keyboards.menu.congress()
    variables.db.user.update(user_id=message.from_user.id, educational_organization=educational_organization)
    await message.answer(
        text="4. Принимали ли Вы участие в Конгрессе молодых ученых и/или Всероссийском Съезде СМУ и СНО?",
        reply_markup=keyboard
    )

@menu_state_router.message(F.text, StateFilter(MenuStates.email))
async def email(message: Message, state: FSMContext, variables: Variables):
    email = message.text
    variables.db.user.update(user_id=message.from_user.id, email=email)
    await state.set_state(MenuStates.consent)
    keyboard = await variables.keyboards.menu.consent_keyboard()
    await message.answer(
        text="📋 <b>Согласие на обработку персональных данных</b>\n\n"
             "Для продолжения работы с ботом необходимо дать согласие на обработку ваших персональных данных.\n\n"
             "Пожалуйста, ознакомьтесь с документом согласия и подтвердите свое согласие.",
        reply_markup=keyboard
    )
