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
    "backstory": "Предыстория"
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

def format_weapons_and_armor(data: dict) -> str:
    """
    Форматирует вывод амуниции и брони
    
    Args:
        data (dict): Словарь с данными персонажа
    
    Returns:
        str: Отформатированный текст с амуницией и броней персонажа
    """
    card = ""

    if "weapons_and_equipment" in data:
        weapons_and_equipment = data["weapons_and_equipment"]
        card += f"*_Амуниция:_*\n```Амуниция\n"
        for name, details in weapons_and_equipment.items():
            card += f"{name}:\n"
            for key, value in details.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                card += align_text([translate_key(key), value], 22) + "\n"
            card += "\n"
    else:
        card += "*_Амуниция: Нет данных_*\n"

    if "armor" in data:
        armor = data["armor"]
        for name, details in armor.items():
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
    else:
        card += ""
    card += "```"
    return card

def convert_json_to_char_info(data: dict) -> str:
    """
    Создает лист персонажа по словарю с данными
    
    Args:
        data (dict): Словарь с данными персонажа
        
    Returns:    
        str: Отформатированный текст с листом персонажа
    """
    card = (
        f'*_\U00002E3A {data.get('name', 'Безымянный')} {data.get('surname', '')} \U00002E3A_*\n\n'
        "*_Основные параметры:_*\n"
        "```Параметры\n"
        f"{align_text(['Возраст', data.get('age', 'Не указан')], 22)}\n"
        f"{align_text(['Раса', data.get('race', 'Не указана')], 22)}\n"
        f"{align_text(['Класс', data.get('character_class', 'Не указан')], 22)}\n"
        f"{align_text(['Уровень', data.get('lvl', 'Не указан')], 22)}\n"
        f"{align_text(['Хиты', data.get('hp', 'Не указаны')], 22)}\n"
        f"{align_text(['Пассивное восприятие', data.get('passive_perception', 'Не указано')], 22)}\n"
        f"{align_text(['Скорость', data.get('speed', 'Не указана')], 22)} футов\n"
        f"{align_text(['Мировоззрение', data.get('worldview', 'Не указано')], 22)}\n"
        f"{align_text(['Инициатива', data.get('initiative', 'Не указана')], 22)}\n"
        f"{align_text(['Вдохновение', 'Да' if data.get('inspiration', False) else 'Нет'], 22)}"
        "```\n\n"
        f"*_Предыстория:_*\n>{tg_text_convert(data.get('backstory', 'Нет данных'))}\n\n\n"
    )

    if 'stats' in data:
        stats = data['stats']
        card += "*_Характеристики:_*\n```Характеристики\n"
        card += "\n".join(align_text([translate_stat(stat), value], 22) for stat, value in stats.items()) + "```"

    if 'stat_modifiers' in data:
        modifiers = data['stat_modifiers']
        card += "\n\n*_Модификаторы характеристик:_*\n```Модификаторы\n"
        card += "\n".join(align_text([translate_stat(stat), value], 22) for stat, value in modifiers.items()) + "```"

    if 'skills' in data:
        skills = data['skills']
        card += "\n\n*_Навыки:_*\n"
        card += "\n".join(f">\U00002022 {skill}" for skill in skills)

    if 'traits_and_abilities' in data:
        traits = data['traits_and_abilities']
        card += "\n\n\n*_Черты и способности:_*\n"
        card += "\n".join(f">\U00002022 *{trait}* – {tg_text_convert(desc)}" for trait, desc in traits.items())

    card += f'\n\n\n {format_weapons_and_armor(data)}'

    if 'inventory' in data:
        inventory = data['inventory']
        card += "\n\n*_Инвентарь:_*\n"
        card += "\n".join(f">\U00002022 {tg_text_convert(item)}" for item in inventory)

    if 'languages' in data:
        languages = data['languages']
        card += "\n\n\n*_Языки:_*\n"
        card += "\n".join(f">\U00002022 {tg_text_convert(language)}" for language in languages)
        
    return card
