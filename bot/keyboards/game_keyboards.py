from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from converter import word_formation


game_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать партию", callback_data="create_game")],
        [InlineKeyboardButton(text="Найти партию", callback_data="find_game")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])

game_type_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открытая", callback_data="Открытая")],
        [InlineKeyboardButton(text="Закрытая", callback_data="Закрытая")]
    ])

game_format_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Онлайн", callback_data="Онлайн")],
        [InlineKeyboardButton(text="Оффлайн", callback_data="Оффлайн")]
    ])

game_level_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Лёгкий", callback_data="Лёгкий")],
        [InlineKeyboardButton(text="Средний", callback_data="Средний")],
        [InlineKeyboardButton(text="Сложный", callback_data="Сложный")],
        [InlineKeyboardButton(text="Социальный", callback_data="Социальный")]
    ])

create_game_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать партию", callback_data="create_game")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])

game_type_filter_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открытая", callback_data="Открытая")],
        [InlineKeyboardButton(text="Закрытая", callback_data="Закрытая")],
        [InlineKeyboardButton(text="Очистить фильтр", callback_data="clear_filter")]
    ])

game_format_filter_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Онлайн", callback_data="Онлайн")],
        [InlineKeyboardButton(text="Оффлайн", callback_data="Оффлайн")],
        [InlineKeyboardButton(text="Очистить фильтр", callback_data="clear_filter")]
    ])

game_level_filter_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Лёгкий", callback_data="Лёгкий")],
        [InlineKeyboardButton(text="Средний", callback_data="Средний")],
        [InlineKeyboardButton(text="Сложный", callback_data="Сложный")],
        [InlineKeyboardButton(text="Социальный", callback_data="Социальный")],
        [InlineKeyboardButton(text="Очистить фильтр", callback_data="clear_filter")]
    ])

clear_filter_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Очистить фильтр", callback_data="clear_filter")]
    ])

create_game_filter_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать партию", callback_data="create_game")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])

request_join_game_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Запросить присоединение к партии", callback_data="request_join_game")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])

create_new_characrer_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать нового", callback_data="create_char")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])

choose_game_character_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать персонажа", callback_data="choose_char")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])

join_game_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Присоединиться к партии", callback_data="join_game")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])

async def url_join_game_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Присоединиться к партии", url=url)],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])

async def copy_seed_keyboard(seed: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Копировать сид", copy_text=CopyTextButton(text=seed))]
    ])

async def game_params_keyboard(
        game_params: dict = {
            "type": None,
            "format": None,
            "city": None,
            "level": None,
            "player_count": None,
            "name": None,
            "description": None
        }
    ) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру для меню с данными о партии.

    Args:
        game_params (dict): Словарь с данными о партии.

    Returns:
        InlineKeyboardMarkup: Итоговая клавиатура.
    """
    if game_params["description"]:
        description = "Описание ✓"
    else:
        description = "Описание"
    player_count = game_params["player_count"]
    if str(player_count).isdigit():
        player_count = await word_formation(int(game_params["player_count"]), 'игрок', 'игрока', 'игроков')
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=game_params["type"] if game_params["type"] else "Тип", callback_data="type"),
         InlineKeyboardButton(text=game_params["format"] if game_params["format"] else "Формат", callback_data="format")],
        [InlineKeyboardButton(text=game_params["city"].capitalize() if game_params["city"] else "Город", callback_data="city"),
         InlineKeyboardButton(text=game_params["level"] if game_params["level"] else "Уровень", callback_data="level")],
        [InlineKeyboardButton(text=player_count if player_count else "Количество игроков", callback_data="player_count"),
          InlineKeyboardButton(text=game_params["name"] if game_params["name"] else "Название", callback_data="name")],
        [InlineKeyboardButton(text=description if description else "Описание", callback_data="description"),
         InlineKeyboardButton(text="Создать партию", callback_data="game_ready")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])

async def game_filters_keyboard(
        game_params: dict = {
            "type": None,
            "format": None,
            "city": None,
            "level": None,
            "player_count": None,
            "name": None
        }
    ) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру для меню с данными о партии.

    Args:
        game_params (dict): Словарь с данными о партии.

    Returns:
        InlineKeyboardMarkup: Итоговая клавиатура.
    """
    player_count = game_params["player_count"]
    if str(player_count).isdigit():
        player_count = await word_formation(int(game_params["player_count"]), 'игрок', 'игрока', 'игроков')
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=game_params["type"] if game_params["type"] else "Тип", callback_data="type"),
         InlineKeyboardButton(text=game_params["format"] if game_params["format"] else "Формат", callback_data="format")],
        [InlineKeyboardButton(text=game_params["city"].capitalize() if game_params["city"] else "Город", callback_data="city"),
         InlineKeyboardButton(text=game_params["level"] if game_params["level"] else "Уровень", callback_data="level")],
        [InlineKeyboardButton(text=player_count if player_count else "Количество игроков", callback_data="player_count"),
          InlineKeyboardButton(text=game_params["name"] if game_params["name"] else "Название", callback_data="name")],
        [InlineKeyboardButton(text="Войти через сид", callback_data="find_game_seed"),
          InlineKeyboardButton(text="Очистить фильтры", callback_data="clear_filters")],
        [InlineKeyboardButton(text="Назад", callback_data="back"),
         InlineKeyboardButton(text="Поиск партий", callback_data="find_game")]
    ])
