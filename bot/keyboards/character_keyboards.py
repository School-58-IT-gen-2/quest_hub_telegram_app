from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


characters_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список персонажей", callback_data="view_characters")],[InlineKeyboardButton(text="Создать нового", callback_data="create_character")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

races_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дварф", callback_data="Дварф"),InlineKeyboardButton(text="Эльф", callback_data="Эльф"),InlineKeyboardButton(text="Полурослик", callback_data="Полурослик")],
        [InlineKeyboardButton(text="Человек", callback_data="Человек"),InlineKeyboardButton(text="Драконид", callback_data="Драконорожденный"),InlineKeyboardButton(text="Гном", callback_data="Гном")],
        [InlineKeyboardButton(text="Полуэльф", callback_data="Полуэльф"),InlineKeyboardButton(text="Полуорк", callback_data="Полуорк"),InlineKeyboardButton(text="Тифлинг", callback_data="Тифлинг")],
        [InlineKeyboardButton(text="Назад", callback_data="char_back")] 
    ])

classes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следопыт", callback_data="Следопыт"),InlineKeyboardButton(text="Варвар", callback_data="Варвар"),InlineKeyboardButton(text="Бард", callback_data="Бард")],
        [InlineKeyboardButton(text="Плут", callback_data="Плут"),InlineKeyboardButton(text="Друид", callback_data="Друид"),InlineKeyboardButton(text="Колдун", callback_data="Колдун")],
        [InlineKeyboardButton(text="Монах", callback_data="Монах"),InlineKeyboardButton(text="Паладин", callback_data="Паладин"),InlineKeyboardButton(text="Жрец", callback_data="Жрец")],
        [InlineKeyboardButton(text="Маг", callback_data="Маг"),InlineKeyboardButton(text="Воин", callback_data="Воин"),InlineKeyboardButton(text="Волшебник", callback_data="Волшебник")],
        [InlineKeyboardButton(text="Назад", callback_data="char_back")] 
    ]) 

gender_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="M"),InlineKeyboardButton(text="Женский", callback_data="W")],
        [InlineKeyboardButton(text="Назад", callback_data="char_back")]
    ])

change_or_delete_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить персонажа", callback_data="put_character")],
        [InlineKeyboardButton(text="Удалить персонажа", callback_data="delete_character")],
        [InlineKeyboardButton(text="Перегенерировать персонажа", callback_data="regenerate_character_from_put")],
        [InlineKeyboardButton(text="Назад", callback_data="view_characters")],
    ])

change_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="char_name"),InlineKeyboardButton(text="Возраст", callback_data="char_age"),InlineKeyboardButton(text="Фамилия",callback_data="char_surname")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_char_from_generation")]])

put_change_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="put_char_name"),InlineKeyboardButton(text="Возраст", callback_data="put_char_age"),InlineKeyboardButton(text="Фамилия",callback_data="put_char_surname")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_char_from_put")]])

character_card_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Инвентарь", callback_data="inventory"), InlineKeyboardButton(text="О персонаже", callback_data="main_char_info")],
        [InlineKeyboardButton(text="Заметки", callback_data="notes"), InlineKeyboardButton(text="Заклинания", callback_data="spells")],
        [InlineKeyboardButton(text="Черты и способноси", callback_data="traits"), InlineKeyboardButton(text="Уровень", callback_data="lvl")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_character"), InlineKeyboardButton(text="Перегенерировать", callback_data="regenerate_character_from_put")],
        [InlineKeyboardButton(text="Назад", callback_data="view_characters")],
    ])

inventory_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опыт", callback_data="exp"),InlineKeyboardButton(text="Золото", callback_data="gold")],[InlineKeyboardButton(text="Предметы",callback_data="items"), InlineKeyboardButton(text="Амуниция",callback_data="ammunition")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

edit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить", callback_data="edit")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

main_char_info_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="name"),InlineKeyboardButton(text="Возраст", callback_data="age")],[InlineKeyboardButton(text="Предыстория",callback_data="backstory"), InlineKeyboardButton(text="Языки",callback_data="languages")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

item_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить название", callback_data="change_name")],
        [InlineKeyboardButton(text="Изменить описание", callback_data="change_desc")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

note_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить название", callback_data="change_title")],
        [InlineKeyboardButton(text="Изменить содержание", callback_data="change_text")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_note")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

name_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить имя", callback_data="change_name")],
        [InlineKeyboardButton(text="Изменить фамилию", callback_data="change_surname")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить язык", callback_data="delete_language")],
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

async def change_keyboard_page(callback_data: str, buttons: list, button_rows: int = 3) -> InlineKeyboardMarkup:
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
