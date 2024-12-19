from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Персонажи", callback_data="characters")],[InlineKeyboardButton(text="Профиль", callback_data="profile")],[InlineKeyboardButton(text="Назначить сессию", callback_data="arrange_meeting")]
    ])

def account_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="change_profile")],[InlineKeyboardButton(text="Удалить аккаунт", callback_data="delete_profile")],[InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]
    ])

def session_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новая сессия", callback_data="new_session")],[InlineKeyboardButton(text="Отменить", callback_data="delete_session")],[InlineKeyboardButton(text="Посмотреть имеющиеся", callback_data="view_session")],
        [InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]
    ])

def yes_or_no_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes")],[InlineKeyboardButton(text="Нет", callback_data="no")]
    ])

def characters_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть 1", callback_data="view_character")],[InlineKeyboardButton(text="Создать нового", callback_data="create_character")],[InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]
    ])

def how_to_create_character_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать самому", callback_data="create_by_myself")],[InlineKeyboardButton(text="Быстрое создание персонажа", callback_data="auto_create")],[InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]
    ])

def change_user_data_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],[InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]])


def race_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Человек", callback_data="human"),InlineKeyboardButton(text="Эльф", callback_data="elf")],
        [InlineKeyboardButton(text="Гном", callback_data="gnome"),InlineKeyboardButton(text="Полуорк", callback_data="halforc")],
        [InlineKeyboardButton(text="Тифлинг", callback_data="tifling"),InlineKeyboardButton(text="Полурослик", callback_data="halfling")],
        [InlineKeyboardButton(text="Драконорожденный", callback_data="dragonborn")],
        [InlineKeyboardButton(text="Главная страница", callback_data="main_menu")] 
    ])


def classes_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следопыт", callback_data="pathfinder"),InlineKeyboardButton(text="Варвар", callback_data="barbarian")],
        [InlineKeyboardButton(text="Бард", callback_data="bard"),InlineKeyboardButton(text="Плут", callback_data="dodger")],
        [InlineKeyboardButton(text="Друид", callback_data="druid"),InlineKeyboardButton(text="Колдун", callback_data="magician")],
        [InlineKeyboardButton(text="Монах", callback_data="monk"),InlineKeyboardButton(text="Паладин", callback_data="paladin")],
        [InlineKeyboardButton(text="Жрец", callback_data="priest"),InlineKeyboardButton(text="Маг", callback_data="warlock")],
        [InlineKeyboardButton(text="Воин", callback_data="warrior"),InlineKeyboardButton(text="Волшебник", callback_data="wizzard")],
        [InlineKeyboardButton(text="Главная страница", callback_data="main_menu")] 
    ]) 


def gender_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="male"),InlineKeyboardButton(text="Женский", callback_data="female")],
        [InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]
    ])



def tier_list_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="S", callback_data="S"),InlineKeyboardButton(text="A", callback_data="A")],
        [InlineKeyboardButton(text="B", callback_data="B"),InlineKeyboardButton(text="C", callback_data="C")],
        [InlineKeyboardButton(text="D", callback_data="D"),InlineKeyboardButton(text="E", callback_data="E")],
        [InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]
    ])


def s_tier_list_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пол персонажа", callback_data="gender"),InlineKeyboardButton(text="Имя", callback_data="name")],
        [InlineKeyboardButton(text="Раса", callback_data="race"),InlineKeyboardButton(text="Класс", callback_data="class")],
        [InlineKeyboardButton(text="Главная страница", callback_data="main_menu")]
    ])