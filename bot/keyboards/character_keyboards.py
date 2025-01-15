from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


characters_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список персонажей", callback_data="view_characters")],[InlineKeyboardButton(text="Создать нового", callback_data="create_character")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

races_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дварф", callback_data="Дварф"),InlineKeyboardButton(text="Эльф", callback_data="Эльф")],
        [InlineKeyboardButton(text="Полурослик", callback_data="Полурослик"),InlineKeyboardButton(text="Человек", callback_data="Человек")],
        [InlineKeyboardButton(text="Драконорожденный", callback_data="Драконорожденный"),InlineKeyboardButton(text="Гном", callback_data="Гном")],
        [InlineKeyboardButton(text="Полуэльф", callback_data="Полуэльф"),InlineKeyboardButton(text="Полуорк", callback_data="Полуорк"),InlineKeyboardButton(text="Тифлинг", callback_data="Тифлинг")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")] 
    ])

classes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следопыт", callback_data="Следопыт"),InlineKeyboardButton(text="Варвар", callback_data="Варвар"),InlineKeyboardButton(text="Бард", callback_data="Бард")],
        [InlineKeyboardButton(text="Плут", callback_data="Плут"),InlineKeyboardButton(text="Друид", callback_data="Друид"),InlineKeyboardButton(text="Колдун", callback_data="Колдун")],
        [InlineKeyboardButton(text="Монах", callback_data="Монах"),InlineKeyboardButton(text="Паладин", callback_data="Паладин"),InlineKeyboardButton(text="Жрец", callback_data="Жрец")],
        [InlineKeyboardButton(text="Маг", callback_data="Маг"),InlineKeyboardButton(text="Воин", callback_data="Воин"),InlineKeyboardButton(text="Волшебник", callback_data="Волшебник")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")] 
    ]) 

gender_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="M"),InlineKeyboardButton(text="Женский", callback_data="W")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

what_do_next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сохранить персонажа", callback_data="save_character")],
        [InlineKeyboardButton(text="Изменить какие-то параметры", callback_data="update_character")],
        [InlineKeyboardButton(text="Удалить персонажа", callback_data="discard_character")],
        [InlineKeyboardButton(text="Перегенерировать персонажа", callback_data="regenerate_character")],
    ])

change_or_delete_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить какие-то параметры", callback_data="put_character")],
        [InlineKeyboardButton(text="Удалить персонажа", callback_data="delete_character")],
        [InlineKeyboardButton(text="Назад", callback_data="view_characters")],
    ])

change_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="char_name"),InlineKeyboardButton(text="Возраст", callback_data="char_age"),InlineKeyboardButton(text="Фамилия",callback_data="char_surname")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_char_from_generation")]])

put_change_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="put_char_name"),InlineKeyboardButton(text="Возраст", callback_data="put_char_age"),InlineKeyboardButton(text="Фамилия",callback_data="put_char_surname")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_char_from_put")]])

async def build_char_kb(chars):
    """Создает клавиатуру с персонажами пользователя"""
    try:
        names = [[i["name"], i["surname"], str(i["id"])] for i in chars]
        inline_kb = []
        for i in names:
            inline_kb.append([InlineKeyboardButton(text=f"{i[0]} {i[1]}", callback_data=i[2])])
    except:
        inline_kb = []
    inline_kb.append([InlineKeyboardButton(text="Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)