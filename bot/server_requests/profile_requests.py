import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_user(tg_id: int) -> dict:
    """
    Запрос на получение пользователя.
    
    Args:
        tg_id (int): ID пользователя в Telegram.

    Returns:
        dict: Словарь с данными пользователя.
    """
    response = httpx.get(f'{os.getenv("QUESTHUB_URL")}/api/v1/profiles/profile',params={"tg_id": tg_id})
    return response.json()

async def create_user(user_data: dict) -> dict: 
    """
    Запрос на создание пользователя.
    
    Args:
        user_data (dict): Словарь с данными пользователя.

    Returns:
        dict: Словарь с данными нового пользователя.
    """
    response = httpx.post(f'{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user',json=user_data)
    return response.json()

async def update_user(user_data: dict) -> dict:
    """
    Запрос на обновление данных пользователя.
    
    Args:
        user_data (dict): Словарь с данными пользователя.

    Returns:
        dict: Словарь с новыми данными пользователя.
    """
    filtered_user_data = {k: v for k, v in user_data.items() if k in ["tg_id","first_name","username","age","last_name","is_premium","language_code"]}
    response = httpx.put(f'{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user',json=filtered_user_data)
    return response.json()

async def delete_user(tg_id: int) -> dict:
    """
    Запрос на удаление пользователя.
    
    Args:
        tg_id (int): ID пользователя в Telegram.

    Returns:
        dict: Словарь с данными удалённого пользователя.
    """
    response = httpx.delete(f'{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user',params={"tg_id": tg_id})
    return response.json()