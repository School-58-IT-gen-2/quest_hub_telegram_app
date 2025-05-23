import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_item(char_id: str, item_id: str) -> dict:
    """
    Запрос на получение предмета из инвенторя.

    Args:
        char_id (str): ID персонажа в базе данных.
        item_id (str): ID предмета в базе данных.

    Returns:
        dict: Словарь с данными предмета.
    """
    response = httpx.get(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory', params={"item_id": item_id})
    return response.json()

async def add_item(char_id: str, item: dict) -> dict:
    """
    Запрос на добавление предмета в инвентарь.

    Args:
        char_id (str): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными добавленного предмета.
    """
    response = httpx.post(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory',json=item)
    return response.json()

async def delete_item(char_id: str, item_id: str) -> dict:
    """
    Запрос на удаление предмета из инвенторя.

    Args:
        char_id (str): ID персонажа в базе данных.
        item_id (str): ID предмета в базе данных.

    Returns:
        dict: Словарь с данными удалённого предмета.
    """
    response = httpx.delete(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory', params={"item_id": item_id})
    return response.json()

async def update_item(char_id: str, item: dict) -> dict:
    """
    Запрос на изменение предмета в инвентаре.

    Args:
        char_id (str): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными обновлённого предмета.
    """
    response = httpx.put(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory',json=item)
    return response.json()

async def get_ammunition(char_id: str, item_id: str) -> dict:
    """
    Запрос на получение снаряжения из амуниции.

    Args:
        char_id (str): ID персонажа в базе данных.
        item_id (str): ID предмета в базе данных.

    Returns:
        dict: Словарь с данными предмета.
    """
    response = httpx.get(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition', params={"item_id": item_id})
    return response.json()

async def add_ammunition(char_id: str, item: dict) -> dict:
    """
    Запрос на добавление снаряжения в амуницию.

    Args:
        char_id (str): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными добавленного предмета.
    """
    response = httpx.post(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition',json=item)
    return response.json()

async def delete_ammunition(char_id: str, item_id: str) -> dict:
    """
    Запрос на удаление снаряжения из амуниции.

    Args:
        char_id (str): ID персонажа в базе данных.
        item_id (str): ID предмета в базе данных.

    Returns:
        dict: Словарь с данными удалённого предмета.
    """
    response = httpx.delete(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition', params={"item_id": item_id})
    return response.json()

async def update_ammunition(char_id: str, item: dict) -> dict:
    """
    Запрос на изменение снаряжения в амуниции.

    Args:
        char_id (str): ID персонажа в базе данных.
        item (dict): Словарь с данными о предмете.

    Returns:
        dict: Словарь с данными обновлённого предмета.
    """
    response = httpx.put(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition',json=item)
    return response.json()

async def update_gold(char_id: str, gold: str) -> dict:
    """
    Запрос на изменение количества золота у персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        gold (str): Количество золота, которое надо добавить/убрать.

    Returns:
        dict: Обновлённое количество золота.
    """
    response = httpx.put(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/gold',json={"gold": gold})
    return response.json()

async def update_experience(char_id: str, experience: str) -> dict:
    """
    Запрос на изменение количества опыта у персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        experience (str): Количество опыта, которое надо добавить/убрать.

    Returns:
        dict: Обновлённое количество опыта.
    """
    response = httpx.put(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/experience',json={"experience": experience})
    return response.json()