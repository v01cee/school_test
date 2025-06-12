from aiogram.fsm.state import StatesGroup, State


class MenuStates(StatesGroup):
    test1 = State()
    test2 = State()
    registration = State()
    educational_organization = State()
    email = State()