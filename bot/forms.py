from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    delete_profile_confirm = State()
    get_user_age = State()
    view_character = State()
    enter_char_class = State()
    enter_char_race = State()
    enter_char_gender = State()