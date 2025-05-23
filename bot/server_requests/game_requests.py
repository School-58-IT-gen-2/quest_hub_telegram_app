import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_game(game_id: str) -> dict:
    """
    Запрос на получение партии.
    
    Args:
        game_id (str): ID партии в базе данных.

    Returns:
        dict: Словарь с данными партии.
    """
    response = httpx.get(f'{os.getenv("QUESTHUB_URL")}/api/v1/games/view_game',params={"game_id": game_id})
    return response.json()

async def get_game_filters(filters: dict) -> list:
    """
    Запрос на получение всех партии, учитывая фильтры.
    
    Returns:
        list: Список с найденными партиями.
    """
    response = httpx.get(f'{os.getenv("QUESTHUB_URL")}/api/v1/games/view_game_with_params', params=filters)
    return response.json()

async def create_game(game_data: dict) -> dict: 
    """
    Запрос на создание партии.
    
    Args:
        game_data (dict): Словарь с данными о партии.

    Returns:
        dict: Словарь с данными новой партии.
    """
    response = httpx.post(f'{os.getenv("QUESTHUB_URL")}/api/v1/games/create',json=game_data)
    return response.json()

async def update_game(game_data: dict) -> dict:
    """
    Запрос на обновление данных партии.
    
    Args:
        game_data (dict): Словарь с данными партии.

    Returns:
        dict: Словарь с новыми данными партии.
    """
    response = httpx.put(f'{os.getenv("QUESTHUB_URL")}/api/v1/games/update_game',json=game_data)
    return response.json()

async def delete_game(game_id: str) -> dict:
    """
    Запрос на удаление партии.
    
    Args:
        game_id (str): ID партии в базе данных.

    Returns:
        dict: Словарь с данными удалённой партии.
    """
    response = httpx.delete(f'{os.getenv("QUESTHUB_URL")}/api/v1/games/delete_game',params={"game_id": game_id})
    return response.json()