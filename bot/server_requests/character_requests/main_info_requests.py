import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def update_name(char_id: str, name: str) -> dict:
    """
    Запрос на изменение имени персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        name (str): Новое имя персонажа.

    Returns:
        dict: Новое имя персонажа.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/name",json={"new_name": name})
    return response.json()

async def update_surname(char_id: str, surname: str) -> dict:
    """
    Запрос на изменение фамилии персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        surname (str): Новая фамилия персонажа.

    Returns:
        dict: Новая фамилия персонажа.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/surname",json={"new_surname": surname})
    return response.json()

async def update_age(char_id: str, age: int) -> dict:
    """
    Запрос на изменение возраста персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        age (int): Новый возраст персонажа.

    Returns:
        dict: Новый возраст персонажа.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/age",json={"new_age": age})
    return response.json()

async def update_backstory(char_id: str, backstory: str) -> dict:
    """
    Запрос на изменение предыстории персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        backstory (str): Новая предыстория персонажа.

    Returns:
        dict: Новая предыстория персонажа.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/backstory",json={"new_backstory": backstory})
    return response.json()

async def add_language(char_id: str, language: str) -> dict:
    """
    Запрос на добавление языка пероснажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        language (str): Название языка.

    Returns:
        dict: Добавленный язык.
    """
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/languages", json={"language": language})
    return response.json()

async def delete_language(char_id: str, language: str) -> dict:
    """
    Запрос на удаление языка пероснажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        language (str): Название языка.

    Returns:
        dict: Удалённый язык.
    """
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/languages", params={"language": language})
    return response.json()