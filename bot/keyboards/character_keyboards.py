from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


characters_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список персонажей", callback_data="view_characters")],[InlineKeyboardButton(text="Создать нового", callback_data="create_character")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

races_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дварф", callback_data="Дварф"),InlineKeyboardButton(text="Эльф", callback_data="Эльф"),InlineKeyboardButton(text="Полурослик", callback_data="Полурослик")],
        [InlineKeyboardButton(text="Человек", callback_data="Человек"),InlineKeyboardButton(text="Драконорожденный", callback_data="Драконорожденный"),InlineKeyboardButton(text="Гном", callback_data="Гном")],
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

main_char_info_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="name"),InlineKeyboardButton(text="Возраст", callback_data="age")],[InlineKeyboardButton(text="Предыстория",callback_data="backstory"), InlineKeyboardButton(text="Языки",callback_data="languages")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

async def build_char_kb(chars: list, page: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с персонажами пользователя"""
    names = [[i["name"], i["surname"], str(i["id"])] for i in chars][page * 6:]
    inline_kb = []
    if len(names) <= 3:
        for i in names:
            inline_kb.append([InlineKeyboardButton(text=f"{i[0]} {i[1]}", callback_data=f"{i[2]}")])
    else:
        for i in range(0, min(len(names) - 1, 5), 2):
            inline_kb.append([InlineKeyboardButton(text=f"{names[i][0]} {names[i][1]}", callback_data=f"{names[i][2]}"), InlineKeyboardButton(text=f"{names[i+1][0]} {names[i+1][1]}", callback_data=f"{names[i+1][2]}")])
        if len(names) == 5:
            inline_kb.append([InlineKeyboardButton(text=f"{names[4][0]} {names[4][1]}", callback_data=f"{names[4][2]}")])
        
    inline_kb.append([InlineKeyboardButton(text="⬅️", callback_data=f"char_left_{page}"), InlineKeyboardButton(text="Назад", callback_data="characters"), InlineKeyboardButton(text="➡️", callback_data=f"char_right_{page}")])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)