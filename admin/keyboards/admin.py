from core.operation import KeyboardOperations



class AdminKeyboard(KeyboardOperations):
    path = "menu"
    async def admin(self):
        buttons = {
            "Выгрузить таблицу с данными": "table_admin",
            "Назад": self.path
        }
        return await self.create_keyboard(buttons=buttons)