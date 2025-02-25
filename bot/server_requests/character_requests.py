import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_char_by_char_id(char_id: int) -> dict:
    """
    Запрос на получение персонажа по его ID в базе данных.
    
    Args:
        char_id (int): ID персонажа в базе данных.

    Returns:
        dict: Словарь с данными персонажа.
    """
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}")
    return response.json() 

async def create_char(char_data: dict) -> dict:
    """
    Запрос на создание персонажа по словарю с данными.

    Args:
        char_data (dict): Словарь с данными персонажа.

    Returns:
        dict: Словарь с данными нового персонажа.
    """
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_data)
    return response.json()

async def update_char(char_data: dict, char_id: int) -> dict:
    """
    Запрос на обновление данных персонажа по словарю с данными и его ID в базе данных.
    
    Args:
        char_data (dict): Словарь с данными персонажа.
        char_id (int): ID персонажа в базе данных.

    Returns:
        dict: Словарь с новыми данными персонажа.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_data,params={"character_id": char_id})
    return response.json()

async def delete_char(char_id: int) -> dict:
    """
    Запрос на удаление персонажа по его ID в базе данных.
    
    Args:
        char_id (int): ID персонажа в базе данных.

    Returns:
        dict: Словарь с данными удалённого персонажа.
    """
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}")
    return response.json()

async def get_char_by_user_id(user_id: str) -> list:
    """
    Запрос на получение всех персонажей пользователя.
    
    Args:
        user_id (str): ID пользователя в базе данных.

    Returns:
        list: Список со всеми персонажами пользователя.
    """
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{user_id}/")
    return response.json()

async def auto_create_char(auto_char_data: dict) -> dict:
    """
    Запрос на автоматическую генерацию персонажа.

    Args:
        auto_char_data (dict): Словарь с полом, расой и классом персонажа.

    Returns:
        dict: Словарь с данными сгенерированного персонажа.
    """
    response = httpx.post(f"{os.getenv("RND_URL")}/create-character-list",json=auto_char_data)
    return response.json()

async def add_item(char_id: int, item: dict) -> dict:
    """Запрос на добавление предмета в инвентарь.

    Args:
        char_id (int): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными добавленного предмета.
    """
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/inventory",json=item)
    return response.json()

async def delete_item(char_id: int, item: dict) -> dict:
    """Запрос на удаление предмета из инвентаря.

    Args:
        char_id (int): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными удалённого предмета.
    """
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/inventory",json=item)
    return response.json()

async def update_item(char_id: int, item: dict) -> dict:
    """Запрос на изменение предмета в инвентаре.

    Args:
        char_id (int): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными обновлённого предмета.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/inventory",json=item)
    return response.json()

async def add_ammunition(char_id: int, item: dict) -> dict:
    """Запрос на добавление снаряжения в амуницию.

    Args:
        char_id (int): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными добавленного предмета.
    """
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/ammunition",json=item)
    return response.json()

async def delete_ammunition(char_id: int, item: dict) -> dict:
    """Запрос на удаление снаряжения из амуниции.

    Args:
        char_id (int): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными удалённого предмета.
    """
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/ammunition",json=item)
    return response.json()

async def update_ammunition(char_id: int, item: dict) -> dict:
    """Запрос на изменение снаряжения в амуниции.

    Args:
        char_id (int): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными обновлённого предмета.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/ammunition",json=item)
    return response.json()

async def add_note(char_id: int, note: dict) -> dict:
    """Запрос на заметки к персонажу.

    Args:
        char_id (int): ID персонажа в базе данных.
        note (dict): Словарь с данными о заметкке.

    Returns:
        dict: Словарь с данными добавленной заметки.
    """
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/notes",json=note)
    return response.json()

async def delete_note(char_id: int, note: dict) -> dict:
    """Запрос на удаление заметки к персонажу.

    Args:
        char_id (int): ID персонажа в базе данных.
        note (dict): Словарь с данными о заметкке.

    Returns:
        dict: Словарь с данными удалённой заметки.
    """
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/notes",json=note)
    return response.json()

async def update_note(char_id: int, note: dict) -> dict:
    """Запрос на изменение заметки к персонажу.

    Args:
        char_id (int): ID персонажа в базе данных.
        note (dict): Словарь с данными о заметкке.

    Returns:
        dict: Словарь с данными обновлённой заметки.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/notes",json=note)
    return response.json()

async def update_gold(char_id: int, gold: int) -> dict:
    """Запрос на изменение количества золота у персонажа.

    Args:
        char_id (int): ID персонажа в базе данных.
        gold (int): Новое количество золота.

    Returns:
        dict: Обновлённое количество золота.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/gold",params={"gold": gold})
    return response.json()

async def update_experience(char_id: int, experience: int) -> dict:
    """Запрос на изменение количества опыта у персонажа.

    Args:
        char_id (int): ID персонажа в базе данных.
        experience (int): Новое количество опыта.

    Returns:
        dict: Обновлённое количество опыта.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}/experience",params={"experience": experience})
    return response.json()