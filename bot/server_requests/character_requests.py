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

async def get_item(char_id: str, item_id: str) -> dict:
    """
    Запрос на получение предмета из инвенторя.

    Args:
        char_id (str): ID персонажа в базе данных.
        item_id (str): ID предмета в базе данных.

    Returns:
        dict: Словарь с данными предмета.
    """
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory", params={"item_id": item_id})
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
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory",json=item)
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
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory", params={"item_id": item_id})
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
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/inventory",json=item)
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
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition", params={"item_id": item_id})
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
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition",json=item)
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
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition", params={"item_id": item_id})
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
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/ammunition",json=item)
    return response.json()

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

async def update_gold(char_id: str, gold: str) -> dict:
    """
    Запрос на изменение количества золота у персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        gold (str): Количество золота, которое надо добавить/убрать.

    Returns:
        dict: Обновлённое количество золота.
    """
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/gold",json={"gold": gold})
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
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/experience",json={"experience": experience})
    return response.json()

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

async def get_trait(char_id: str, trait_id: str) -> dict:
    """
    Запрос на получение особенности персонажа.

    Args:
        char_id (str): ID персонажа в базе данных.
        trait_id (str): ID особенности в базе данных.

    Returns:
        dict: Словарь с данными особенности.
    """
    response = httpx.get(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities", params={"trait_id": trait_id})
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
    response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities",json=trait)
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
    response = httpx.delete(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities",params={"trait_id": trait_id})
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
    response = httpx.put(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/{char_id}/traits_and_abilities",json=trait)
    return response.json()