from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    delete_profile_confirm = State()
    delete_character_confirm = State()
    discard_character = State()
    get_user_age = State()
    view_character = State()
    auto_char_class = State()
    auto_char_race = State()
    auto_char_gender = State()