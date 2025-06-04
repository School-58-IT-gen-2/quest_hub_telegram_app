TRANSLATIONS = {
    "type": "Тип",
    "damage": "Урон",
    "damage_type": "Тип урона",
    "properties": "Свойства",
    "weight": "Вес",
    "cost": "Цена",
    "ac_base": "Базовая защита (AC)",
    "dex_bonus": "Бонус Ловкости",
    "max_dex_bonus": "Макс. бонус Ловкости",
    "stealth_disadvantage": "Помеха скрытности",
    "weapons": "Оружие",
    "armor": "Броня",
    "name": "Имя",
    "surname": "Фамилия",
    "race": "Раса",
    "character_class": "Класс",
    "lvl": "Уровень",
    "hp": "Хиты",
    "speed": "Скорость",
    "worldview": "Мировоззрение",
    "initiative": "Инициатива",
    "inspiration": "Вдохновение",
    "stats": "Характеристики",
    "stat_modifiers": "Модификаторы характеристик",
    "skills": "Навыки",
    "traits_and_abilities": "Черты и способности",
    "inventory": "Инвентарь",
    "languages": "Языки",
    "backstory": "Предыстория",
    "range": "Дальность",
    "duration": "Длительность",
    "components": "Компоненты",
    "description": "Описание",
    "casting_time": "Время накладывания",
    "count": "Количество"
}

async def translate_key(key: str) -> str:
    """
    Переводит название параметра на русский.

    Args:
        key (str): Название параметра на английском.

    Returns:
        str: Название параметра на русском.
    """
    return TRANSLATIONS.get(key, key)

async def translate_stat(stat: str) -> str:
    """
    Переводит название характеристики на русский.
    
    Args:
        stat (str): Название характеристики на английском.

    Returns:
        str: Название характеристики на русском.
    """
    stat_translations = {
        'strength': 'Сила',
        'dexterity': 'Ловкость',
        'constitution': 'Выносливость',
        'intelligence': 'Интеллект',
        'wisdom': 'Мудрость',
        'charisma': 'Харизма'
    }
    return stat_translations.get(stat, stat.capitalize())

async def tg_text_convert(text: str) -> str:
    """
    Форматирует текст для отправки в Telegram.
    
    Args:
        text (str): Текст, который надо отформатировать.

    Returns:
        str: Отформатированный текст.
    """
    restricted_symbols = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for i in restricted_symbols:
        text = text.replace(i, '\\' + i)
    return text

async def word_formation(count: int, form_1: str, form_2: str, form_3: str) -> str:
    """
    Склоняет слово в зависимости от количества предметов.
    
    Args:
        count (int): Количество предметов.
        form_1 (str): Склонение слова, если предмет 1.
        form_2 (str): Склонение слова, если предметов от 2 до 4 (или 0).
        form_2 (str): Склонение слова в остальных случаях.

    Returns:
        str: Строка с нужным склонением слова..
    """
    last_digit = count % 10
    if last_digit == 0 or last_digit >= 5 or (count % 100) in range(11, 19):
        result = f'{count} {form_3}'
    elif last_digit == 1:
        result = f'{count} {form_1}'
    else:
        result = f'{count} {form_2}'
    return result

async def align_text(text: list, offset: int = 22, max_column_length: int = 18) -> str:
    """
    Выравнивает текст в 2 столбца.

    Args:
        text (str): Список из 2 элементов (текст в двух колонках).
        offset (int): Расстояние между началом первого и второго столбца в символах.

    Returns:
        str: Отформатированный текст.
    """
    if len(str(text[1])) <= max_column_length:
        return f"{text[0]}:" + ' ' * (offset - len(text[0])) + str(text[1])
    right_column = str(text[1]).split()
    right_row = ''
    right_rows = []
    if len(str(text[1])) > max_column_length:
        i = 0
        while i < len(right_column):
            while len(right_row + right_column[i]) < max_column_length:
                right_row += f' {right_column[i]}'
                i += 1
                if i == len(right_column):
                    break
            right_rows.append(right_row)
            right_row = ''
    result_string = f"{text[0]}:" + ' ' * (offset - len(text[0]) - 1) + right_rows[0]
    for i in range(1, len(right_rows)):
        result_string += '\n' + ' ' * offset + right_rows[i]
    return result_string

async def check_int(string: str) -> bool:
        """
        Определяет, является ли строка целым числом.

        Args:
            string (str): Строка для проверки.
        
        Returns:
            bool: Выводит правду или ложь.
        """
        if string[0] in ('-', '+'):
            return string[1:].isdigit()
        return string.isdigit()

async def format_ammunition(data: dict) -> dict:
    """
    Форматирует вывод амуниции и брони.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        dict: Словарь с отформатированным снаряжением.
    """
    weapons_and_equipment = data["weapons_and_equipment"]
    weapons_dict = dict()
    for weapon in weapons_and_equipment:
        card = f'```Амуниция\n{weapon["name"]}\n'
        for key, value in weapon.items():
            description = ""
            if key == "dex_bonus":
                value = "Да" if value else "Нет"
            elif key == "stealth_disadvantage":
                value = "Да" if value else "Нет"
            elif key == 'weight' and value:
                value = await word_formation(int(value), 'фунт', 'фунта', 'фунтов')
            elif key == 'cost' and value:
                value = await word_formation(int(value), 'золотой', 'золотых', 'золотых')
            elif key == 'count' and value:
                value = int(value)
                value = f'{value} шт.'
            if isinstance(value, list):
                value = ", ".join(value)
            if key == "description" and value:
                description = value
            elif key != "name" and key != "id" and value:
                card += await align_text([await translate_key(key), value], 22) + "\n"
            card += description
        weapons_dict[weapon["id"]] = card + '```'
        card = ""
    return weapons_dict

async def format_inventory(data: dict) -> dict:
    """
    Форматирует вывод предметов инвентаря.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        dict: Словарь с отформатированными предметами.
    """
    invenotry = data["inventory"]
    invenotry_dict = dict()
    for item in invenotry:
        card = f'```Снаряжение\n{item["name"]}\n'
        for key, value in item.items():
            description = ""
            if key == "dex_bonus":
                value = "Да" if value else "Нет"
            elif key == "stealth_disadvantage":
                value = "Да" if value else "Нет"
            elif key == 'weight' and value:
                value = await word_formation(int(value), 'фунт', 'фунта', 'фунтов')
            elif key == 'cost' and value:
                value = await word_formation(int(value), 'золотой', 'золотых', 'золотых')
            elif key == 'count' and value:
                value = int(value)
                value = f'{value} шт.'
            if isinstance(value, list):
                value = ", ".join(value)
            if key == "description" and value:
                description = value
            elif key != "name" and key != "id" and value:
                card += await align_text([await translate_key(key), value], 22) + "\n"
            card += description
        invenotry_dict[item["id"]] = card + '```'
        card = ""
    return invenotry_dict

async def format_spells(data: dict) -> str:
    """
    Форматирует вывод заклинаний.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        str: Отформатированные заклинания.
    """
    card = "```Заклинания"
    spells = data["spells"]
    description = ""
    if spells:
        for name, details in spells.items():
            card += f"\n{name}\n"
            for key, value in details.items():
                if key == 'description':
                    description = value
                else:
                    card += await align_text([await translate_key(key), value], 22) + "\n"
            card += description + '\n'
        card += '```'
    else:
        card = '\nУ вашего персонажа нет заклинаний\.'
    return card

async def format_notes(data: dict) -> dict:
    """
    Форматирует вывод заметок.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        dict: Словарь с отформатированными заметками.
    """
    notes = data["notes"]
    notes_dict = dict()
    if notes:
        for note in notes:
            notes_dict[note["id"]] = f'*_{await tg_text_convert(note["title"])}_*\n\n{await tg_text_convert(note["text"])}'
    return notes_dict

async def format_traits(data: dict) -> dict:
    """
    Форматирует вывод черт и способностей.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        dict: Словарь с отформатированными чертами и способностями.
    """
    traits = data["traits_and_abilities"]
    traits_dict = dict()
    if traits:
        for trait in traits:
            traits_dict[trait["id"]] = f'*_{await tg_text_convert(trait["name"])}_*\n\n{await tg_text_convert(trait["description"])}'
    return traits_dict

async def game_card(game_params: dict) -> str:
    text = f"```Партия\n{game_params["name"]}\n"
    text += await align_text(['Формат', game_params["format"]]) + '\n'
    text += await align_text(['Тип', game_params["type"]]) + '\n'
    if game_params["format"] == "Оффлайн":
        text += await align_text(['Город', game_params["city"].capitalize()]) + '\n'
    if game_params["level"]:
        text += await align_text(['Уровень', game_params["level"]]) + '\n'
    if "char_id" in game_params:
        player_count = f'{len(game_params["char_id"])}/{game_params["player_count"]}'
    else:
        player_count = await word_formation(int(game_params["player_count"]), 'игрок', 'игрока', 'игроков')
    text += await align_text(['Количество игроков', player_count]) + '\n'
    if game_params["description"]:
        text += game_params["description"]
    text += '```'
    return text

async def character_card(data: dict) -> dict:
    """
    Создает лист персонажа по словарю с данными.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        dict: Словарь с отформатированными параметрами персонажа.
    """
    age = '*_' + (await word_formation(data.get('age', 'Не указан'), 'год', 'года', 'лет')) + '_*'
    
    card = (
        f'*_\U00002E3A {await tg_text_convert(data.get('name', 'Безымянный'))} {await tg_text_convert(data.get('surname', ''))} \U00002E3A_*\n\n'
        "👤 *_Основные параметры:_*\n"
        "```Параметры\n"
        f"{await align_text(['Возраст', age[2:-2]], 22)}\n"
        f"{await align_text(['Раса', data.get('subrace', 'Не указана') if data.get('subrace', 'Не указана') else data.get('race', 'Не указана')], 22)}\n"
        f"{await align_text(['Класс', data.get('character_class', 'Не указан')], 22)}\n"
        f"{await align_text(['Уровень', 1 if data.get('lvl', 'Не указан') == None else data.get('lvl', 'Не указан')], 22)}\n"
        f"{await align_text(['Хиты', data.get('hp', 'Не указаны')], 22)}\n"
        f"{await align_text(['Пассивное восприятие', data.get('passive_perception', 'Не указано')], 22)}\n"
        f"{await align_text(['Скорость', data.get('speed', 'Не указана')], 22)} футов\n"
        f"{await align_text(['Мировоззрение', data.get('worldview', 'Не указано')], 22)}\n"
        f"{await align_text(['Инициатива', data.get('initiative', 'Не указана')], 22)}\n"
        f"{await align_text(['Вдохновение', 'Да' if data.get('inspiration', False) else 'Нет'], 22)}"
        "```\n\n"
    )

    if 'stats' in data:
        stats = data['stats']
        modifiers = data['stat_modifiers']
        card += "📊  *_Характеристики:_*\n```Характеристики\n"
        stat_arr = []
        for i in range(len(stats)):
            stat = list(stats.keys())[i]
            value = list(stats.values())[i]
            modifier = list(modifiers.values())[i]
            if modifier >= 0:
                modifier = "+" + str(modifier)
            modifier = str(modifier)
            stat_arr.append(await align_text([await translate_stat(stat), f'({value})'], 22) + ' ' * (4 - len(str(value))) + modifier)
        card += "\n".join(stat_arr) + "```"

    if 'skills' in data:
        skills = data['skills']
        card += "\n\n🛠️ *_Навыки:_*\n"
        card += "\n".join(f">\U00002022 {skill}" for skill in skills)

    name = f'*_{await tg_text_convert(data.get('name', 'Безымянный'))} {await tg_text_convert(data.get('surname', ''))}_*'

    backstory = f"📜 *_Предыстория:_*\n\n>" + "\n>".join((await tg_text_convert(data.get('backstory', 'Нет данных'))).split('\n'))

    ammunition = await format_ammunition(data)

    spells = await format_spells(data)

    inventory = await format_inventory(data)

    notes = await format_notes(data)

    traits_and_abilities = await format_traits(data)

    languages = [[i, i] for i in data['languages']]
        
    return {"name": name, "age": age, "main_char_info": card, "backstory": backstory, "traits_and_abilities": traits_and_abilities, "ammunition": ammunition, "spells": spells, "inventory": inventory, "notes": notes, "languages": languages}

async  def game_character_card(data: dict) -> str:
    """
    Создает лист персонажа по словарю с данными.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        str: Отформатированный текст с листом персонажа.
    """
    char_dict = await character_card(data)
    traits = data["traits_and_abilities"]
    traits_and_abilities = 'Нет данных'
    if traits:
        traits_and_abilities = '\n>'.join([f'\U00002022 *_{await tg_text_convert(trait["name"])}_* – {await tg_text_convert(trait["description"])}' for trait in traits])
    languages_data = data["languages"]
    languages = 'Нет данных'
    if languages_data:
        languages = '\n>\U00002022 '.join(languages_data)
    char_list = char_dict["main_char_info"]
    char_list += '\n\n\n🧬 *_Черты и способности:_*\n>' + traits_and_abilities
    char_list += '\n\n\n🗣️ *_Языки:_*\n>\U00002022 ' + languages
    char_list += '\n\n\n🪄 *_Заклинания:_*\n'
    if data['spells']:
        char_list += char_dict['spells']
    else:
        char_list += '>У персонажа нет заклинаний\.'
    return char_list