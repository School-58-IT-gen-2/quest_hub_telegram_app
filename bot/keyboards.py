from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Персонажи", callback_data="characters")],[InlineKeyboardButton(text="Профиль", callback_data="profile")],[InlineKeyboardButton(text="Назначить сессию", callback_data="arrange_meeting")]
    ])

account_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="change_profile")],[InlineKeyboardButton(text="Удалить профиль", callback_data="delete_profile")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

session_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новая сессия", callback_data="new_session")],[InlineKeyboardButton(text="Отменить", callback_data="delete_session")],[InlineKeyboardButton(text="Посмотреть имеющиеся", callback_data="view_session")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

yes_or_no_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes"), InlineKeyboardButton(text="Нет", callback_data="no")]
    ])

characters_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список персонажей", callback_data="view_characters")],[InlineKeyboardButton(text="Создать нового", callback_data="create_character")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

how_to_create_character_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать самому", callback_data="create_by_myself")],[InlineKeyboardButton(text="Быстрое создание персонажа", callback_data="auto_create")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

change_user_data_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]])

race_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Человек", callback_data="human"),InlineKeyboardButton(text="Эльф", callback_data="elf")],
        [InlineKeyboardButton(text="Гном", callback_data="gnome"),InlineKeyboardButton(text="Полуорк", callback_data="halforc")],
        [InlineKeyboardButton(text="Тифлинг", callback_data="tifling"),InlineKeyboardButton(text="Полурослик", callback_data="halfling")],
        [InlineKeyboardButton(text="Драконорожденный", callback_data="dragonborn")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")] 
    ])

classes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следопыт", callback_data="pathfinder"),InlineKeyboardButton(text="Варвар", callback_data="barbarian"),InlineKeyboardButton(text="Бард", callback_data="bard")],
        [InlineKeyboardButton(text="Плут", callback_data="dodger"),InlineKeyboardButton(text="Друид", callback_data="druid"),InlineKeyboardButton(text="Колдун", callback_data="magician")],
        [InlineKeyboardButton(text="Монах", callback_data="monk"),InlineKeyboardButton(text="Паладин", callback_data="paladin"),InlineKeyboardButton(text="Жрец", callback_data="priest"),InlineKeyboardButton(text="Маг", callback_data="warlock")],
        [InlineKeyboardButton(text="Воин", callback_data="warrior"),InlineKeyboardButton(text="Волшебник", callback_data="wizzard")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")] 
    ]) 

gender_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="male"),InlineKeyboardButton(text="Женский", callback_data="female")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

char_list_keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пол персонажа", callback_data="gender"),InlineKeyboardButton(text="Имя", callback_data="name")],
        [InlineKeyboardButton(text="Раса", callback_data="race"),InlineKeyboardButton(text="Класс", callback_data="class")],
        [InlineKeyboardButton(text="Очки здоровья", callback_data="hp"),InlineKeyboardButton(text="Скорость", callback_data="speed")],
        [InlineKeyboardButton(text="⏪", callback_data="null_data"), InlineKeyboardButton(text="⬅️", callback_data="null_data"), InlineKeyboardButton(text="➡️", callback_data="page_2"), InlineKeyboardButton(text="⏩", callback_data="page_5")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

char_list_keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Навыки", callback_data="skills"),InlineKeyboardButton(text="Пассивные навыки", callback_data="passive_perception")],
        [InlineKeyboardButton(text="Спасиброски способности", callback_data="ability_saving_throws"),InlineKeyboardButton(text="Спасброски от смерти", callback_data="death_saving_throws")],
        [InlineKeyboardButton(text="Снаряжение", callback_data="weapons_and_equipment"),InlineKeyboardButton(text="Мировозрение", callback_data="allignment")],
        [InlineKeyboardButton(text="⏪", callback_data="page_1"), InlineKeyboardButton(text="⬅️", callback_data="page_1"),InlineKeyboardButton(text="➡️", callback_data="page_3"), InlineKeyboardButton(text="⏩", callback_data="page_5")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

char_list_keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Уровень", callback_data="lvl"),InlineKeyboardButton(text="Бонус владения", callback_data="ownership_bonus")],
        [InlineKeyboardButton(text="Атаки и урон", callback_data="attacks_and_damage"),InlineKeyboardButton(text="Опыт", callback_data="experience")],
        [InlineKeyboardButton(text="Черты и способности", callback_data="traits_and_abilities"),InlineKeyboardButton(text="Заклинания и магия", callback_data="spells")],
        [InlineKeyboardButton(text="⏪", callback_data="page_1"), InlineKeyboardButton(text="⬅️", callback_data="page_2"), InlineKeyboardButton(text="➡️", callback_data="page_4"), InlineKeyboardButton(text="⏩", callback_data="page_5")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

char_list_keyboard_4 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Инициатива", callback_data="initiative"),InlineKeyboardButton(text="Предыстория", callback_data="backstory")],
        [InlineKeyboardButton(text="Ценности", callback_data="valuables"),InlineKeyboardButton(text="Языки", callback_data="languages")],
        [InlineKeyboardButton(text="Вмешательство", callback_data="interference"),InlineKeyboardButton(text="Преимущества", callback_data="advantages")],
        [InlineKeyboardButton(text="⏪", callback_data="page_1"), InlineKeyboardButton(text="⬅️", callback_data="page_3"), InlineKeyboardButton(text="➡️", callback_data="page_5"), InlineKeyboardButton(text="⏩", callback_data="page_5")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

char_list_keyboard_5 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Слабости", callback_data="weaknesses"),InlineKeyboardButton(text="Вдохновения", callback_data="inspiration")],
        [InlineKeyboardButton(text="Отношения с персонажами", callback_data="npc_relations"),InlineKeyboardButton(text="Дневник", callback_data="diary")],
        [InlineKeyboardButton(text="Заметки", callback_data="notes")],
        [InlineKeyboardButton(text="⏪", callback_data="page_1"), InlineKeyboardButton(text="⬅️", callback_data="page_4"), InlineKeyboardButton(text="➡️", callback_data="null_data"), InlineKeyboardButton(text="⏩", callback_data="null_data")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

def build_char_kb(chars):
    names = [[i["name"], str(i["id"])] for i in chars]
    inline_kb = []
    for i in names:
        inline_kb.append([InlineKeyboardButton(text=i[0], callback_data=i[1])])
    inline_kb.append([InlineKeyboardButton(text="Главная меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)