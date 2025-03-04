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

def translate_key(key: str) -> str:
    """
    Переводит название параметра на русский.

    Args:
        key (str): Название параметра на английском.

    Returns:
        str: Название параметра на русском.
    """
    return TRANSLATIONS.get(key, key)

def translate_stat(stat: str) -> str:
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

def tg_text_convert(text: str) -> str:
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

def align_text(text: list, offset: int, max_column_length: int = 18) -> str:
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

def check_int(string: str) -> bool:
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

def format_ammunition(data: dict) -> dict:
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
            elif key == 'weight':
                value = int(value)
                last_digit = value % 10
                if last_digit == 0 or last_digit >= 5 or (value % 100) in range(11, 19):
                    value = f'{value} фунтов'
                elif last_digit == 1:
                    value = f'{value} фунт'
                else:
                    value = f'{value} фунта'
            elif key == 'cost':
                value = int(value)
                last_digit = value % 10
                if last_digit == 0 or last_digit >= 5 or (value % 100) in range(11, 19):
                    value = f'{value} золотых'
                elif last_digit == 1:
                    value = f'{value} золотой'
                else:
                    value = f'{value} золотых'
            elif key == 'count':
                value = int(value)
                value = f'{value} шт.'
            if isinstance(value, list):
                value = ", ".join(value)
            if key == "description":
                description = value
            elif key != "name" and key != "id" and value:
                card += align_text([translate_key(key), value], 22) + "\n"
            card += description
        weapons_dict[weapon["id"]] = card + '```'
        card = ""
    return weapons_dict

def format_inventory(data: dict) -> dict:
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
            elif key == 'weight':
                value = int(value)
                last_digit = value % 10
                if last_digit == 0 or last_digit >= 5 or (value % 100) in range(11, 19):
                    value = f'{value} фунтов'
                elif last_digit == 1:
                    value = f'{value} фунт'
                else:
                    value = f'{value} фунта'
            elif key == 'cost':
                value = int(value)
                last_digit = value % 10
                if last_digit == 0 or last_digit >= 5 or (value % 100) in range(11, 19):
                    value = f'{value} золотых'
                elif last_digit == 1:
                    value = f'{value} золотой'
                else:
                    value = f'{value} золотых'
            elif key == 'count':
                value = int(value)
                value = f'{value} шт.'
            if isinstance(value, list):
                value = ", ".join(value)
            if key == "description":
                description = value
            elif key != "name" and key != "id" and value:
                card += align_text([translate_key(key), value], 22) + "\n"
            card += description
        invenotry_dict[item["id"]] = card + '```'
        card = ""
    return invenotry_dict

def format_spells(data: dict) -> str:
    """
    Форматирует вывод заклинаний.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        str: Отформатированные заклинания.
    """
    card = "```Заклинания"
    spells = data["spells"]
    spells_dict = dict()
    if spells:
        for name, details in spells.items():
            card += f"\n{name}\n"
            spell_name = name
            for key, value in details.items():
                if key == 'description':
                    description = value
                else:
                    card += align_text([translate_key(key), value], 22) + "\n"
            card += description + '\n'
        card += '```'
    else:
        card += '\nУ вашего персонажа нет заклинаний\.'
    return card

def format_notes(data: dict) -> dict:
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
            notes_dict[note["id"]] = f'*_{note["title"]}_*\n\n{note["text"]}'
    return notes_dict

def character_card(data: dict) -> dict:
    """
    Создает лист персонажа по словарю с данными.
    
    Args:
        data (dict): Словарь с данными персонажа.
    
    Returns:
        dict: Словарь с отформатированными параметрами персонажа.
    """
    age = data.get('age', 'Не указан')
    last_digit = age % 10
    if last_digit == 0 or last_digit >= 5 or (age % 100) in range(11, 19):
        age = f'*_{age} лет_*'
    elif last_digit == 1:
        age = f'*_{age} год_*'
    else:
        age = f'*_{age} года_*'

    card = (
        f'*_\U00002E3A {data.get('name', 'Безымянный')} {data.get('surname', '')} \U00002E3A_*\n\n'
        "👤 *_Основные параметры:_*\n"
        "```Параметры\n"
        f"{align_text(['Возраст', age[2:-2]], 22)}\n"
        f"{align_text(['Раса', data.get('subrace', 'Не указана') if data.get('subrace', 'Не указана') else data.get('race', 'Не указана')], 22)}\n"
        f"{align_text(['Класс', data.get('character_class', 'Не указан')], 22)}\n"
        f"{align_text(['Уровень', 1 if data.get('lvl', 'Не указан') == None else data.get('lvl', 'Не указан')], 22)}\n"
        f"{align_text(['Хиты', data.get('hp', 'Не указаны')], 22)}\n"
        f"{align_text(['Пассивное восприятие', data.get('passive_perception', 'Не указано')], 22)}\n"
        f"{align_text(['Скорость', data.get('speed', 'Не указана')], 22)} футов\n"
        f"{align_text(['Мировоззрение', data.get('worldview', 'Не указано')], 22)}\n"
        f"{align_text(['Инициатива', data.get('initiative', 'Не указана')], 22)}\n"
        f"{align_text(['Вдохновение', 'Да' if data.get('inspiration', False) else 'Нет'], 22)}"
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
            stat_arr.append(align_text([translate_stat(stat), f'({value})'], 22) + ' ' * (4 - len(str(value))) + modifier)
        card += "\n".join(stat_arr) + "```"

    if 'skills' in data:
        skills = data['skills']
        card += "\n\n🛠️ *_Навыки:_*\n"
        card += "\n".join(f">\U00002022 {skill}" for skill in skills)

    name = f'*_{data.get('name', 'Безымянный')} {data.get('surname', '')}_*'

    backstory = f"📜 *_Предыстория:_*\n>{tg_text_convert(data.get('backstory', 'Нет данных'))}"

    traits_and_abilities = "🧬 *_Черты и способности:_*\n" + "\n".join(f">\U00002022 *{trait}* – {tg_text_convert(desc).lower()}" for trait, desc in data['traits_and_abilities'].items())

    ammunition = format_ammunition(data)

    spells = format_spells(data)

    inventory = format_inventory(data)

    notes = format_notes(data)

    languages = "🗣️ *_Языки:_*\n" + "\n".join(f">\U00002022 {tg_text_convert(language)}" for language in data['languages'])
        
    return {"name": name, "age": age, "main_char_info": card, "backstory": backstory, "traits_and_abilities": traits_and_abilities, "ammunition": ammunition, "spells": spells, "inventory": inventory, "notes": notes, "languages": languages}
