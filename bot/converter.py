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
}

def translate_key(key: str) -> str:
    """Переводит название параметра на русский

    Args:
        key (str): Название параметра на английском

    Returns:
        str: Название параметра на русском
    """
    return TRANSLATIONS.get(key, key)

def translate_stat(stat: str) -> str:
    """
    Переводит название характеристики на русский
    
    Args:
        stat (str): Название характеристики на английском

    Returns:
        str: Название характеристики на русском
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
    Форматирует текст для отправки в ТГ
    
    Args:
        text (str): Текст, который надо отформатировать

    Returns:
        str: Отформатированный текст
    """
    restricted_symbols = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for i in restricted_symbols:
        text = text.replace(i, '\\' + i)
    return text

def align_text(text: list, offset: int) -> str:
    """
    Выравнивает текст в 2 колонки

    Args:
        text (str): Список из 2 элементов (текст в двух колонках)
        offset (int): Расстояние между началом первой и второй колонки в символах

    Returns:
        str: Отформатированный текст
    """
    return f"{text[0]}:" + ' ' * (offset - len(text[0])) + str(text[1])

def format_ammunition(data: dict) -> str:
    """
    Форматирует вывод амуниции и брони
    
    Args:
        data (dict): Словарь с данными персонажа
    
    Returns:
        str: Отформатированный текст с амуницией и броней персонажа
    """
    card = f"*_Амуниция:_*\n```Амуниция\n"
    weapons_and_equipment = data["weapons_and_equipment"]
    for name, details in weapons_and_equipment.items():
        card += f"{name}:\n"
        for key, value in details.items():
            if key == "dex_bonus":
                value = "Да" if value else "Нет"
            elif key == "stealth_disadvantage":
                value = "Да" if value else "Нет"
            if isinstance(value, list):
                value = ", ".join(value)
            card += align_text([translate_key(key), value], 22) + "\n"
        card += "\n"
    card += "```"
    return card

def format_spells(data: dict) -> str:
    """
    Форматирует вывод заклинаний
    
    Args:
        data (dict): Словарь с данными персонажа
    
    Returns:
        str: Отформатированный текст с заклинаниями персонажа
    """
    card = ""
    spells = data["spells"]
    if spells:
        card += f"*_Заклинания:_*\n```Заклинания\n"
        for name, details in spells.items():
            card += f"{name}:\n"
            for key, value in details.items():
                if key == 'description':
                    description = value
                else:
                    card += align_text([translate_key(key), value], 22) + "\n"
            card += description
            card += "\n\n"
        card += "```"
    else:
        card += '*_Заклинания:_*\n\nУ вашего персонажа нет заклинаний\.'
    return card

def character_card(data: dict) -> dict:
    """
    Создает лист персонажа по словарю с данными
    
    Args:
        data (dict): Словарь с данными персонажа
        
    Returns:    
        dict: Словарь с отформатированными параметрами персонажа.
    """
    card = (
        f'*_\U00002E3A {data.get('name', 'Безымянный')} {data.get('surname', '')} \U00002E3A_*\n\n'
        "👤 *_Основные параметры:_*\n"
        "```Параметры\n"
        f"{align_text(['Возраст', data.get('age', 'Не указан')], 22)}\n"
        f"{align_text(['Раса', data.get('race', 'Не указана')], 22)}\n"
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

    age = data.get('age', 'Не указан')
    last_digit = age % 10
    if last_digit == 0 or last_digit >= 5 or age in range(11, 19):
        age = f'*_{age} лет_*'
    elif last_digit == 1:
        age = f'*_{age} год*'
    else:
        age = f'*_{age} года*'

    backstory = f"📜 *_Предыстория:_*\n>{tg_text_convert(data.get('backstory', 'Нет данных'))}"

    traits_and_abilities = "🧬 *_Черты и способности:_*\n" + "\n".join(f">\U00002022 *{trait}* – {tg_text_convert(desc).lower()}" for trait, desc in data['traits_and_abilities'].items())

    ammunition = f'🛡️ {format_ammunition(data)}'

    spells = f'🪄 {format_spells(data)}'

    inventory = "🎒 *_Предметы:_*\n" + "\n".join(f">\U00002022 {tg_text_convert(item)}" for item in data['inventory'])

    languages = "🗣️ *_Языки:_*\n" + "\n".join(f">\U00002022 {tg_text_convert(language)}" for language in data['languages'])
        
    return {"name": name, "age": age, "main_char_info": card, "backstory": backstory, "traits_and_abilities": traits_and_abilities, "ammunition": ammunition, "spells": spells, "inventory": inventory, "languages": languages}