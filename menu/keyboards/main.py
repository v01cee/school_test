from core.operation import KeyboardOperations
from core.utils.photo_id import answers_choices_test1, callbacks_test1, answers_choices_test2, callbacks_test2


class MenuKeyboard(KeyboardOperations):
    path = "menu"
    async def menu(self):
        buttons = {
            "Выбрать тест": "choose_test"
           }
        return await self.create_keyboard(buttons=buttons)

    async def confirm_data(self):
        buttons = {"Даю согласие": "give_confirmation"}
        return await self.create_keyboard(buttons=buttons)

    async def choose_test(self):
        buttons = {
            "Школьник": "group_one",
            "Студент": "group_one",
            "Аспирант/Молодой ученый": "group_two",
            "<- Назад": self.path
        }
        return await self.create_keyboard(buttons=buttons)

    async def confirmation(self, number_test: int):
        buttons = {
            "Начать тест": f"start_test_{number_test}",
            "<- Назад": self.path
        }
        return await self.create_keyboard(buttons=buttons)

    async def test1_question(self, callback_number: int):
        callbacks = callbacks_test1[callback_number]
        buttons = {
            "1 Вариант": callbacks[0],
            "2 Вариант": callbacks[1],
            "3 Вариант": callbacks[2],
            "4 Вариант": callbacks[3]
        }
        return await self.create_keyboard(buttons=buttons)

    async def test2_question(self, callback_number: int):
        callbacks = callbacks_test2[callback_number]
        buttons = {
            "1 Вариант": callbacks[0],
            "2 Вариант": callbacks[1],
            "3 Вариант": callbacks[2],
            "4 Вариант": callbacks[3]
        }
        return await self.create_keyboard(buttons=buttons)

    async def registration_1(self):
        buttons = {
            "Школьник": "status_schoolboy",
            "Студент": "status_student",
            "Аспирант/Молодой ученый": "status_student_graduate"
        }
        return await self.create_keyboard(buttons=buttons)

    async def congress(self):
        buttons = {
            "Да": "congress_yes",
            "Нет": "congress_no"
        }
        return await self.create_keyboard(buttons=buttons)