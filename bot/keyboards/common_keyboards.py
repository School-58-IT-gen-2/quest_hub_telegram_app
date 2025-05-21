from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Персонажи", callback_data="characters")],[InlineKeyboardButton(text="Профиль", callback_data="profile")],[InlineKeyboardButton(text="Партии", callback_data="arrange_meeting")]
    ])

yes_or_no_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes"), InlineKeyboardButton(text="Нет", callback_data="no")]
    ])

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

async def build_arr_keyboard(buttons: list, page: int = 0, button_rows: int = 3) -> list:
    """
    Создает клавиатуру по словарю с данными.
    
    Args:
        buttons (list): Вложенный список, где в каждом внутреннем списке на 0 месте название кнопки, а на 1 – её значение.
        page (int): Номер текущей страницы меню (начиная с нуля).
        button_rows (int): Количество строк с кнопками.

    Returns:
        InlineKeyboardMarkup: Итоговая клавиатура.
    """
    inline_kb = []
    length = len(buttons)
    buttons = buttons[page * button_rows * 2:]
    if len(buttons) <= 3:
        for i in buttons:
            inline_kb.append([InlineKeyboardButton(text=f"{i[0]}", callback_data=f"{i[1]}")])
    else:
        for i in range(0, min(len(buttons) - 1, button_rows * 2 - 1), 2):
            inline_kb.append([InlineKeyboardButton(text=f"{buttons[i][0]}", callback_data=f"{buttons[i][1]}"), InlineKeyboardButton(text=f"{buttons[i+1][0]}", callback_data=f"{buttons[i+1][1]}")])
        if len(buttons) == button_rows * 2 - 1:
            inline_kb.append([InlineKeyboardButton(text=f"{buttons[(button_rows - 1) * 2][0]}", callback_data=f"{buttons[(button_rows - 1) * 2][1]}")])
    if length > button_rows * 2:
        inline_kb.append([InlineKeyboardButton(text="⬅️", callback_data=f"left_{page}"), InlineKeyboardButton(text="Назад", callback_data="dict_kb_back"), InlineKeyboardButton(text="➡️", callback_data=f"right_{page}")])
    else:
        inline_kb.append([InlineKeyboardButton(text="Назад", callback_data="dict_kb_back")])
    return inline_kb

async def change_keyboard_page(callback_data: str, buttons: list, button_rows: int = 3) -> list:
    """
    Обновляет клавиатуру, созданную по словарю, меняя страницу.

    Args:
        callback_data (str): Данные, которые пришли от пользователя.
        buttons (list): Вложенный список, где в каждом внутреннем списке на 0 месте название кнопки, а на 1 – её значение.
        button_rows (int): Количество строк с кнопками.

    Returns:
        InlineKeyboardMarkup: Итоговая клавиатура.
    """
    page = int(callback_data.split('_')[-1])
    direction = -1 if callback_data.split('_')[0] == 'left' else 1
    if -1 < page + direction < -(-len(buttons) // (button_rows * 2)):
       return await build_arr_keyboard(buttons, page + direction, button_rows)
