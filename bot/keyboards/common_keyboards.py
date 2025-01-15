from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Персонажи", callback_data="characters")],[InlineKeyboardButton(text="Профиль", callback_data="profile")],[InlineKeyboardButton(text="Назначить сессию", callback_data="arrange_meeting")]
    ])

yes_or_no_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes"), InlineKeyboardButton(text="Нет", callback_data="no")]
    ])