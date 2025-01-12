from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


session_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новая сессия", callback_data="new_session")],[InlineKeyboardButton(text="Отменить игру", callback_data="delete_session")],[InlineKeyboardButton(text="Посмотреть имеющиеся", callback_data="view_session")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])