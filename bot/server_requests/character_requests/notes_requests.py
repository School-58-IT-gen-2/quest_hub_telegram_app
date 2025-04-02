import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_note(char_id: str, note_id: str) -> dict:
    """
    Запрос на получение заметки к персонажу.

    Args:
        char_id (str): ID персонажа в базе данных.
        note_id (str): ID заметки в базе данных.

    Returns:
        dict: Словарь с данными заметки.
    """
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/notes", params={"note_id": note_id})
    return response.json()

async def add_note(char_id: str, note: dict) -> dict:
    """
    Запрос на добавление заметки к персонажу.

    Args:
        char_id (str): ID персонажа в базе данных.
        note (dict): Словарь с данными о заметкке.

    Returns:
        dict: Словарь с данными добавленной заметки.
    """
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/notes",json=note)
    return response.json()

async def delete_note(char_id: str, note_id: str) -> dict:
    """
    Запрос на удаление заметки к персонажу.

    Args:
        char_id (str): ID персонажа в базе данных.
        note_id (str): ID заметки в базе данных.

    Returns:
        dict: Словарь с данными удалённой заметки.
    """
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/notes",params={"note_id": note_id})
    return response.json()

async def update_note(char_id: str, note: dict) -> dict:
    """
    Запрос на изменение заметки к персонажу.

    Args:
        char_id (str): ID персонажа в базе данных.
        note (dict): Словарь с данными о заметкке.

    Returns:
        dict: Словарь с данными обновлённой заметки.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/notes",json=note)
    return response.json()