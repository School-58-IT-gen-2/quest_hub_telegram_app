import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_trait(char_id: str, trait_id: str) -> dict:
    """
    Запрос на получение особенности персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        trait_id (str): ID особенности в базе данных.

    Returns:
        dict: Словарь с данными особенности.
    """
    response = httpx.get(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities', params={"trait_id": trait_id})
    return response.json()

async def add_trait(char_id: str, trait: dict) -> dict:
    """
    Запрос на добавление особенности персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        abitraitlity (dict): Словарь с данными об особенности.

    Returns:
        dict: Словарь с данными добавленной особенности.
    """
    response = httpx.post(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities',json=trait)
    return response.json()

async def delete_trait(char_id: str, trait_id: str) -> dict:
    """
    Запрос на удаление особенности персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        trait_id (str): ID особенности в базе данных.

    Returns:
        dict: Словарь с данными удалённой особенности.
    """
    response = httpx.delete(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities',params={"trait_id": trait_id})
    return response.json()

async def update_trait(char_id: str, trait: dict) -> dict:
    """
    Запрос на изменение особенности персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        trait (dict): Словарь с данными об особенности.

    Returns:
        dict: Словарь с данными обновлённой особенности.
    """
    response = httpx.put(f'{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities',json=trait)
    return response.json()