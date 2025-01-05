from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    delete_profile_confirm = State()
    get_user_age = State()
    view_character = State()
    auto_char_class = State() # auto_ для генерации от рндшников
    auto_char_race = State()
    auto_char_gender = State()
    enter_char_gender = State() # enter_ для ручного ввода
    enter_char_name = State()