from menu.keyboards.main import MenuKeyboard
from admin.keyboards.admin import AdminKeyboard

class Keyboards:
    def __init__(self):
        self.menu = MenuKeyboard()
        self.admin = AdminKeyboard()