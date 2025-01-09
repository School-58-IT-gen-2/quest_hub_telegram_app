import asyncio

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

def translate_key(key):
    """Translates a key using the TRANSLATIONS dictionary."""
    return TRANSLATIONS.get(key, key)

def translate_stat(stat):
    """Translates stat keys into Russian."""
    stat_translations = {
        'strength': 'Сила',
        'dexterity': 'Ловкость',
        'constitution': 'Выносливость',
        'intelligence': 'Интеллект',
        'wisdom': 'Мудрость',
        'charisma': 'Харизма'
    }
    return stat_translations.get(stat, stat.capitalize())

def format_weapons_and_armor(data):
    """Formats weapons and armor data into a readable text response with translation."""
    card = ""

    # Форматирование оружия и снаряжения
    if "weapons_and_equipment" in data:
        weapons_and_equipment = data["weapons_and_equipment"]
        card += f"*🛡️ Амуниция:*\n"
        for name, details in weapons_and_equipment.items():
            card += f"  - *{name}:*\n"
            for key, value in details.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                # Преобразуем типы данных
                card += f"    - {translate_key(key)}: {value}\n"
            card += "\n"
    else:
        card += "*🛡️ Амуниция: Нет данных*\n"

    # Форматирование брони
    if "armor" in data:
        armor = data["armor"]
        card += ""
        for name, details in armor.items():
            card += f"  - *{name}:*\n"
            for key, value in details.items():
                if key == "dex_bonus":
                    value = "Да" if value else "Нет"
                elif key == "stealth_disadvantage":
                    value = "Да" if value else "Нет"
                if isinstance(value, list):
                    value = ", ".join(value)
                card += f"    - {translate_key(key)}: {value}\n"
            card += "\n"
    else:
        card += ""

    return card


async def convert_json_to_char_info(data: dict):
    card = (
        f"*Карточка персонажа:*\n"
        f"👤 *Имя:* {data.get('name', 'Безымянный')} {data.get('surname', '')}\n"
        f"🎂 *Возраст:* {data.get('age', 'Не указан')}\n"
        f"🌍 *Раса:* {data.get('race', 'Не указана')}\n"
        f"⚔️ *Класс:* {data.get('character_class', 'Не указан')}\n"
        f"🌟 *Уровень:* {data.get('lvl', 'Не указан')}\n"
        f"💓 *Хиты:* {data.get('hp', 'Не указаны')}\n"
        f"👁️ *Пассивное восприятие:* {data.get('passive_perception', 'Не указано')}\n"
        f"🏃 *Скорость:* {data.get('speed', 'Не указана')} футов\n"
        f"⚖️ *Мировоззрение:* {data.get('worldview', 'Не указано')}\n"
        f"🎲 *Инициатива:* {data.get('initiative', 'Не указана')}\n"
        f"💡 *Вдохновение:* {'Да' if data.get('inspiration', False) else 'Нет'}\n"
        f"*📜 Предыстория:*\n{data.get('backstory', 'Нет данных')}\n\n"
    )

    if 'stats' in data:
        stats = data['stats']
        card += "*⚙️ Характеристики:*\n"
        card += "\n".join(f"  - {translate_stat(stat)}: {value}" for stat, value in stats.items())  # Перевод характеристик

    if 'stat_modifiers' in data:
        modifiers = data['stat_modifiers']
        card += "\n\n*📊 Модификаторы характеристик:*\n"
        card += "\n".join(f"  - {translate_stat(stat)}: {value}" for stat, value in modifiers.items())

    if 'skills' in data:
        skills = data['skills']
        card += "\n\n*🛠️ Навыки:*\n"
        card += ", ".join(skills)

    if 'traits_and_abilities' in data:
        traits = data['traits_and_abilities']
        card += "\n\n*🧬 Черты и способности:*\n"
        card += "\n".join(f"  - *{trait}:* {desc}" for trait, desc in traits.items())

    # Форматируем оружие и броню перед инвентарём
    card += f'\n\n {format_weapons_and_armor(data)}'

    # Инвентарь
    if 'inventory' in data:
        inventory = data['inventory']
        card += "\n\n*🎒 Инвентарь:*\n"
        card += ", ".join(inventory)

    if 'languages' in data:
        languages = data['languages']
        card += "\n\n*🗣️ Языки:*\n"
        card += ", ".join(languages)
        
    return card
