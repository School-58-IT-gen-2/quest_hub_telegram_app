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
    char_name = State()
    char_age = State()
    char_surname = State()
    put_char_name = State()
    put_char_age = State()
    put_char_surname = State()
    regenerate_char = State()