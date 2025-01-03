import httpx
import asyncio 
import os
from dotenv import load_dotenv

load_dotenv()

#запросы для пользователя
async def get_user(tg_id: int):
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/profiles/profile",params={"tg_id": tg_id})
    return response.json()

async def create_user(user_data: dict): 
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user",json=user_data)
    return response.json()

async def update_user(user_data: dict):
    filtered_user_data = {k: v for k, v in user_data.items() if k in ["tg_id","first_name","username","age","last_name","is_premium","language_code"]} #фильтруем только на нужные значения
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user",json=filtered_user_data)
    return response.json()

async def delete_user(tg_id: int):
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user",params={"tg_id": tg_id})
    return response.json()

#запросы для персонажей
async def get_char_by_char_id(char_id: int):
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}")
    return response.json() 

async def create_char(char_data: dict):
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_data)
    return response.json()

async def update_char(char_data: dict, char_id: int):
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_data,params={"character_id": char_id})
    return response.json()

async def delete_char(char_id: int):
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{char_id}")
    return response.json()

async def get_char_by_user_id(user_id: int):
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list/{user_id}/")
    return response.json()

#запрос к mvp от rnd
async def auto_create_char(auto_char_data: dict):
    response = httpx.post(f"{os.getenv("RND_URL")}/create-character-list",json=auto_char_data)
    return response.json()