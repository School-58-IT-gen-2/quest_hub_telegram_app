import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_char_by_char_id(char_id: int):
    """Запрос на получение персонажа по его ID в базе данных"""
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}")
    return response.json() 

async def create_char(char_data: dict):
    """Запрос на создание персонажа по словарю с данными"""
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_data)
    return response.json()

async def update_char(char_data: dict, char_id: int):
    """Запрос на обновление данных персонажа по словарю с данными и его ID в базе данных"""
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_data,params={"character_id": char_id})
    return response.json()

async def delete_char(char_id: int):
    """Запрос на удаление персонажа по его ID в базе данных"""
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}")
    return response.json()

async def get_char_by_user_id(user_id: int):
    """Запрос на получение всех персонажей пользователя по ID пользователя в Telegram"""
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{user_id}/")
    return response.json()

async def auto_create_char(auto_char_data: dict):
    """Запрос на автоматическую генерацию листа персонажа"""
    response = httpx.post(f"{os.getenv("RND_URL")}/create-character-list",json=auto_char_data)
    return response.json()