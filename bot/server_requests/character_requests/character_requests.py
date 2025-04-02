import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_char(char_id: str) -> dict:
    """
    Запрос на получение персонажа по его ID в базе данных.
    
    Args:
        char_id (str): ID персонажа в базе данных.

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

async def update_char(char_data: dict, char_id: str) -> dict:
    """
    Запрос на обновление данных персонажа по словарю с данными и его ID в базе данных.
    
    Args:
        char_data (dict): Словарь с данными персонажа.
        char_id (str): ID персонажа в базе данных.

    Returns:
        dict: Словарь с новыми данными персонажа.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_data,params={"character_id": char_id})
    return response.json()

async def delete_char(char_id: str) -> dict:
    """
    Запрос на удаление персонажа по его ID в базе данных.
    
    Args:
        char_id (str): ID персонажа в базе данных.

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