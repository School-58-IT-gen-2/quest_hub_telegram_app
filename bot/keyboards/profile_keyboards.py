from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


account_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="change_profile")],[InlineKeyboardButton(text="Удалить профиль", callback_data="delete_profile")], [InlineKeyboardButton(text="Статистика", callback_data="profile_stats")], [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

change_user_data_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]])
