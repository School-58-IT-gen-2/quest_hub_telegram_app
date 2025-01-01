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
    print(filtered_user_data)
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user",json=filtered_user_data)
    return response.json()

async def delete_user(tg_id: int):
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/profiles/user",params={"tg_id": tg_id})
    return response.json()


