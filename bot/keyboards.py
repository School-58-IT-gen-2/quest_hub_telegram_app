from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Персонажи", callback_data="characters")],[InlineKeyboardButton(text="Профиль", callback_data="profile")],[InlineKeyboardButton(text="Назначить сессию", callback_data="arrange_meeting")]
    ])

account_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="change_profile")],[InlineKeyboardButton(text="Удалить профиль", callback_data="delete_profile")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

session_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новая сессия", callback_data="new_session")],[InlineKeyboardButton(text="Отменить игру", callback_data="delete_session")],[InlineKeyboardButton(text="Посмотреть имеющиеся", callback_data="view_session")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

yes_or_no_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes"), InlineKeyboardButton(text="Нет", callback_data="no")]
    ])

characters_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список персонажей", callback_data="view_characters")],[InlineKeyboardButton(text="Создать нового", callback_data="create_character")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

change_user_data_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]])

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
        [InlineKeyboardButton(text="Монах", callback_data="Монах"),InlineKeyboardButton(text="Паладин", callback_data="Паладин"),InlineKeyboardButton(text="Жрец", callback_data="Жрец"),InlineKeyboardButton(text="Маг", callback_data="Маг")],
        [InlineKeyboardButton(text="Воин", callback_data="Воин"),InlineKeyboardButton(text="Волшебник", callback_data="Волшебник")],
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
    ])

change_or_delete_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить какие-то параметры", callback_data="update_character")],
        [InlineKeyboardButton(text="Удалить персонажа", callback_data="delete_character")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])

change_character = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="char_name"),InlineKeyboardButton(text="Возраст", callback_data="char_age"),InlineKeyboardButton(text="Фамилия",callback_data="char_surname")]])


async def build_char_kb(chars):
    names = [[i["name"], str(i["id"])] for i in chars]
    inline_kb = []
    for i in names:
        inline_kb.append([InlineKeyboardButton(text=i[0], callback_data=i[1])])
    inline_kb.append([InlineKeyboardButton(text="Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)