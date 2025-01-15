from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


account_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="change_profile")],[InlineKeyboardButton(text="Удалить профиль", callback_data="delete_profile")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

change_user_data_keyboard = InlineKeyboardMarkup(inline_keyboard=[
<<<<<<< HEAD
        [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]])
=======
        [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]])
>>>>>>> 603cedb1e1fe5f189c0626ecf3752f81ae7a2410
