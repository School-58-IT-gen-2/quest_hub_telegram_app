from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

create_method_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Быстро", callback_data="quick_create")],
        [InlineKeyboardButton(text="⚙️ Подробно", callback_data="detailed_create")]
    ])

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

item_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить название", callback_data="change_name")],
        [InlineKeyboardButton(text="Изменить описание", callback_data="change_desc")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

note_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить название", callback_data="change_title")],
        [InlineKeyboardButton(text="Изменить содержание", callback_data="change_text")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_note")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

trait_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить название", callback_data="change_name")],
        [InlineKeyboardButton(text="Изменить описание", callback_data="change_description")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_trait")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

name_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить имя", callback_data="change_name")],
        [InlineKeyboardButton(text="Изменить фамилию", callback_data="change_surname")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить язык", callback_data="delete_language")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]])


def get_keyboard(options: list, add_random=True, add_back=True):
    builder = InlineKeyboardBuilder()
    for opt in options:
        builder.button(text=opt, callback_data=opt)
    if add_random:
        builder.button(text="🎲 Случайно", callback_data="__random__")
    if add_back:
        builder.button(text="⬅️ Назад", callback_data="__back__")
    builder.adjust(2)
    return builder.as_markup()