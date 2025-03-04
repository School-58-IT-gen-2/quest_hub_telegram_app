import asyncio
import json
import random

from aiogram import Dispatcher, types, Router
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests import *
from handlers.commands import main_menu, main_menu_query
from forms import Form
from converter import *


dp = Dispatcher()
router = Router()

@router.callback_query(lambda c: c.data == 'characters')
async def characters(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню персонажей"""
    await callback_query.answer()
    await state.clear()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)

@router.callback_query(lambda c: c.data == 'view_characters')
async def view_characters(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие списка всех персонажей пользователя"""
    await callback_query.answer()
    await state.clear()
    user_chars = await get_char_by_user_id(callback_query.from_user.id)
    if len(user_chars) == 0:
        await callback_query.message.edit_caption(caption="У вас ещё нет персонажей", reply_markup=characters_keyboard)
    else:
        char_dict = dict()
        for char in user_chars:
            char_dict[f'{char["name"]} {char["surname"]}'] = str(char["id"])
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=await build_dict_keyboard(char_dict))
        await state.set_state(Form.view_character)

@router.callback_query(Form.view_character)
async def view_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Вывод персонажа"""
    await callback_query.answer()
    if 'left' in callback_query.data or 'right' in callback_query.data:
        user_chars = await get_char_by_user_id(callback_query.from_user.id)
        char_dict = dict()
        for char in user_chars:
            char_dict[f'{char["name"]} {char["surname"]}'] = str(char["id"])
        await callback_query.message.edit_caption(reply_markup=await change_keyboard_page(callback_query.data, char_dict))
    elif callback_query.data == "dict_kb_back":
        await characters(callback_query, state)
    else:
        char = await get_char(int(callback_query.data))
        char = char[0]
        await callback_query.message.delete()
        await callback_query.message.answer(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)
        await state.update_data({"char": char})

@router.callback_query(Form.character_card)
async def view_char_params(callback_query: types.CallbackQuery, state: FSMContext):
    """Вывод отдельных параметров песонажа персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "inventory":
        await callback_query.message.edit_text(text='📋 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    if callback_query.data == "notes":
        notes_dict = dict()
        if char["notes"]:
            for note in char["notes"]:
                notes_dict[note["title"]] = note["id"]
        await callback_query.message.edit_text(text='✏️ *_Заметки:_*', reply_markup=await build_notes_keyboard(notes_dict),parse_mode="MarkdownV2")
        await state.set_state(Form.notes_menu)
    if callback_query.data == "traits":
        await callback_query.message.edit_text(text=character_card(char)["traits_and_abilities"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.traits_menu)
    if callback_query.data == "main_char_info":
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)
    if callback_query.data == "lvl":
        await callback_query.message.edit_text(text=f'*_Текущий уровень:_* {char['lvl'] if char['lvl'] else 1}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.lvl_menu)
    if callback_query.data == "spells":
        await callback_query.message.edit_text(text='🪄 *_Заклинания:_*\n' + character_card(char)["spells"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.spells_menu)
    if callback_query.data == 'delete_character':
        await callback_query.message.edit_text(text="Удалённого персонажа невозможно восстановить. Продолжить?", reply_markup=yes_or_no_keyboard)
        await state.set_state(Form.delete_character_confirm)
    if callback_query.data == 'regenerate_character_from_put':
        await callback_query.message.edit_text(text="Весь текущий прогресс персонажа будет утерян. Продолжить?", reply_markup=yes_or_no_keyboard)
        await state.set_state(Form.regenerate_char)

@router.callback_query(Form.notes_menu)
async def notes_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заметки персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        notes_dict = dict()
        if char["notes"]:
            for note in char["notes"]:
                notes_dict[note["title"]] = note["id"]
        await callback_query.message.edit_caption(reply_markup=await change_notes_keyboard_page(callback_query.data, notes_dict))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)
    elif callback_query.data == "create_note":
        await callback_query.message.edit_text(text="Введите название новой заметки:")
        await state.set_state(Form.create_note_title)
    else:
        await state.set_state(Form.note_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=character_card(char)["notes"][callback_query.data], reply_markup=note_keyboard, parse_mode="MarkdownV2")

@router.message(Form.create_note_title)
async def create_note_title(message: types.Message, state: FSMContext):
    """Создание заметки"""
    title = message.text
    await state.update_data({"note_title": title})
    await message.answer(text="Введите содержание новой заметки:")
    await state.set_state(Form.create_note_text)

@router.message(Form.create_note_text)
async def create_note_text(message: types.Message, state: FSMContext):
    """Создание заметки"""
    text = message.text
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    title = data["note_title"]
    note = {"title": title, "text": text}
    note = await add_note(char_id, note)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.note_menu)
    await state.update_data({"item_id": note["id"]})
    await message.answer(text=character_card(char)["notes"][note["id"]], reply_markup=note_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.note_menu)
async def note_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заметка персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        notes_dict = dict()
        if char["notes"]:
            for note in char["notes"]:
                notes_dict[note["title"]] = note["id"]
        await callback_query.message.edit_text(text='✏️ *_Заметки:_*', reply_markup=await build_notes_keyboard(notes_dict),parse_mode="MarkdownV2")
        await state.set_state(Form.notes_menu)
    elif callback_query.data == "change_title":
        await callback_query.message.edit_text(text=f'{character_card(char)["notes"][item_id]}\n\nВведите новое название:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_note_title)
    elif callback_query.data == "change_text":
        await callback_query.message.edit_text(text=f'{character_card(char)["notes"][item_id]}\n\nВведите новое содержание:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_note_text)

@router.message(Form.change_note_title)
async def change_note_title(message: types.Message, state: FSMContext):
    """Изменение названия заметки"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_note(char_id, item_id)
    item["title"] = message.text
    item = await update_note(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.inventory_item_menu)
    await message.answer(text=character_card(char)["notes"][item_id], reply_markup=note_keyboard, parse_mode="MarkdownV2")

@router.message(Form.change_note_text)
async def change_note_text(message: types.Message, state: FSMContext):
    """Изменение содержание заметки"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_note(char_id, item_id)
    item["text"] = message.text
    item = await update_note(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.inventory_item_menu)
    await message.answer(text=character_card(char)["notes"][item_id], reply_markup=note_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.main_char_info_menu)
async def main_char_info_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Основные сведения о персонаже"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "name":
        await callback_query.message.edit_text(text=character_card(char)["name"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.name_menu)
    if callback_query.data == "age":
        await callback_query.message.edit_text(text=character_card(char)["age"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.age_menu)
    if callback_query.data == "backstory":
        await callback_query.message.edit_text(text=character_card(char)["backstory"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.backstory_menu)
    if callback_query.data == "languages":
        await callback_query.message.edit_text(text=character_card(char)["languages"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.languages_menu)
    if callback_query.data == "back":
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.traits_menu)
async def traits_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Черты и особенности персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.spells_menu)
async def spells_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заклинания персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.lvl_menu)
async def lvl_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Уровень персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.name_menu)
async def name_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Имя персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)

@router.callback_query(Form.age_menu)
async def age_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Возраст персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)

@router.callback_query(Form.backstory_menu)
async def backstory_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предыстория персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)

@router.callback_query(Form.languages_menu)
async def languages_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Языки персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)

@router.callback_query(Form.inventory_menu)
async def inventory(callback_query: types.CallbackQuery, state: FSMContext):
    """Инвентарь персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "items":
        item_dict = dict()
        for item in char["inventory"]:
            item_dict[item["name"]] = item["id"]
        await callback_query.message.edit_text(text=f'🛠️ *_Снаряжение:_*', reply_markup=await build_dict_keyboard(item_dict),parse_mode="MarkdownV2")
        await state.set_state(Form.items_menu)
    if callback_query.data == "ammunition":
        ammunition_dict = dict()
        for weapon in char["weapons_and_equipment"]:
            ammunition_dict[weapon["name"]] = weapon["id"]
        await callback_query.message.edit_text(text=f'🛡️ *_Амуниция:_*', reply_markup=await build_dict_keyboard(ammunition_dict),parse_mode="MarkdownV2")
        await state.set_state(Form.ammunition_menu)
    if callback_query.data == "exp":
        await callback_query.message.edit_text(text=f'*_Текущий опыт:_* {char['experience']}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.experience_menu)
    if callback_query.data == "gold":
        await callback_query.message.edit_text(text=f'*_Текущее количество золота:_* {char['gold']}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.gold_menu)
    if callback_query.data == "back":
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.items_menu)
async def items_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Снаряжение персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        item_dict = dict()
        for item in char["inventory"]:
            item_dict[item["name"]] = item["id"]
        await callback_query.message.edit_caption(reply_markup=await change_keyboard_page(callback_query.data, item_dict))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text='🎒 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await state.set_state(Form.inventory_item_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=character_card(char)["inventory"][callback_query.data], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.inventory_item_menu)
async def inventory_item_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предмет персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        item_dict = dict()
        for item in char["inventory"]:
            item_dict[item["name"]] = item["id"]
        await callback_query.message.edit_text(text=f'🛠️ *_Снаряжение:_*', reply_markup=await build_dict_keyboard(item_dict),parse_mode="MarkdownV2")
        await state.set_state(Form.items_menu)
    elif callback_query.data == "change_name":
        await callback_query.message.edit_text(text=f'{character_card(char)["inventory"][item_id]}\n\nВведите новое название:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_inventory_item_name)
    elif callback_query.data == "change_desc":
        await callback_query.message.edit_text(text=f'{character_card(char)["inventory"][item_id]}\n\nВведите новое описание:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_inventory_item_desc)

@router.message(Form.change_inventory_item_name)
async def change_inventory_item_name(message: types.Message, state: FSMContext):
    """Изменение названия снаряжения"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_item(char_id, item_id)
    item["name"] = message.text
    item = await update_item(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.inventory_item_menu)
    await message.answer(text=character_card(char)["inventory"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.message(Form.change_inventory_item_desc)
async def change_inventory_item_desc(message: types.Message, state: FSMContext):
    """Изменение описания снаряжения"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_item(char_id, item_id)
    item["description"] = message.text
    item = await update_item(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.inventory_item_menu)
    await message.answer(text=character_card(char)["inventory"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.gold_menu)
async def gold_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Золото персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='🎒 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await callback_query.message.edit_text(text=f'*_Текущее количество золота:_* {char['gold']}\n\nВведите количество золота\, которое вы хотите добавить/убрать\. Например `+10` или `-4`\.',parse_mode="MarkdownV2")
        await state.set_state(Form.change_gold)

@router.message(Form.change_gold)
async def change_gold(message: types.Message, state: FSMContext):
    """Изменить количество золота персонажа"""
    char = await state.get_data()
    char = char["char"]
    char_id = char["id"]
    data = message.text
    if check_int(data):
        if char['gold'] + int(data) < 0:
            await message.answer(text="Вы не можете потратить больше золота, чем у вас есть.")
        else:
            await update_gold(char_id, data)
            char['gold'] += int(data)
            await state.update_data({"char": char})
            await message.answer(text=f'*_Текущее количество золота:_* {char["gold"]}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
            await state.set_state(Form.gold_menu)
    else:
        await message.answer(text="Пожалуйста используйте корректный формат ввода.")

@router.callback_query(Form.ammunition_menu)
async def ammunition_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Амуниция персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        ammunition_dict = dict()
        for weapon in char["weapons_and_equipment"]:
            ammunition_dict[weapon["name"]] = weapon["id"]
        await callback_query.message.edit_caption(reply_markup=await change_keyboard_page(callback_query.data, ammunition_dict))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text='🎒 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await state.set_state(Form.ammunition_item_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=character_card(char)["ammunition"][callback_query.data], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.ammunition_item_menu)
async def ammunition_item_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предмет персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        ammunition_dict = dict()
        for weapon in char["weapons_and_equipment"]:
            ammunition_dict[weapon["name"]] = weapon["id"]
        await callback_query.message.edit_text(text=f'🛡️ *_Амуниция:_*', reply_markup=await build_dict_keyboard(ammunition_dict),parse_mode="MarkdownV2")
        await state.set_state(Form.ammunition_menu)
    elif callback_query.data == "change_name":
        await callback_query.message.edit_text(text=f'{character_card(char)["ammunition"][item_id]}\n\nВведите новое название:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_ammunition_item_name)
    elif callback_query.data == "change_desc":
        await callback_query.message.edit_text(text=f'{character_card(char)["ammunition"][item_id]}\n\nВведите новое описание:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_ammunition_item_desc)

@router.message(Form.change_ammunition_item_name)
async def change_ammunition_item_name(message: types.Message, state: FSMContext):
    """Изменение названия снаряжения"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_ammunition(char_id, item_id)
    item["name"] = message.text
    item = await update_ammunition(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.ammunition_item_menu)
    await message.answer(text=character_card(char)["ammunition"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.message(Form.change_ammunition_item_desc)
async def change_ammunition_item_desc(message: types.Message, state: FSMContext):
    """Изменение описания снаряжения"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_ammunition(char_id, item_id)
    item["description"] = message.text
    item = await update_ammunition(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.ammunition_item_menu)
    await message.answer(text=character_card(char)["ammunition"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.experience_menu)
async def experience_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Опыт персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='🎒 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await callback_query.message.edit_text(text=f'*_Текущий опыт:_* {char['experience']}\n\nВведите количество опыта\, которое вы хотите добавить/убрать\. Например `+12` или `-3`\.',parse_mode="MarkdownV2")
        await state.set_state(Form.change_xp)

@router.message(Form.change_xp)
async def change_xp(message: types.Message, state: FSMContext):
    """Изменить количество опыта персонажа"""
    char = await state.get_data()
    char = char["char"]
    char_id = char["id"]
    data = message.text
    if check_int(data):
        if char['experience'] + int(data) < 0:
            await message.answer(text="У вас не может быть отрицательное количество опыта.")
        else:
            await update_experience(char_id, data)
            char['experience'] += int(data)
            await state.update_data({"char": char})
            await message.answer(text=f'*_Текущий опыт:_* {char["experience"]}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
            await state.set_state(Form.experience_menu)
    else:
        await message.answer(text="Пожалуйста используйте корректный формат ввода.")

@router.callback_query(Form.regenerate_char)
async def regenerate_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Перегенерация персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    data = await state.get_data()
    char_id = data["char"]["id"]
    if callback_query.data == "yes":
        response = await auto_create_char({"gender": char["gender"], "race": char["race"], "character_class": char["character_class"]})
        response["user_id"] = str(callback_query.from_user.id)
        response["name"] = char["name"]
        response["surname"] = char["surname"]
        char = await update_char(response, char_id)
        await state.update_data({"char": char})
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)
    else:
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)

@router.callback_query(Form.delete_character_confirm)
async def delete_character_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню подтверждения удаления персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "yes":
        await delete_char(char["id"])
        await state.clear()
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)
        await callback_query.message.edit_caption(caption="Вы жестоко удалили вашего персонажа!", reply_markup=characters_keyboard)
    if callback_query.data == "no":
        await callback_query.message.edit_text(parse_mode="MarkdownV2",text=f"{character_card(char["main_char_info"])}\n\nВы отказались от удаления персонажа",reply_markup=character_card_keyboard)

@router.callback_query(lambda c: c.data == 'back')
async def get_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Возврат к просмотру персонажа"""
    await callback_query.answer()
    await callback_query.message.delete()
    await state.set_state(Form.view_character)

@router.callback_query(lambda c: c.data == 'create_character')
async def choose_creation(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие меню с выбором класса персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/char_create.png")))
    await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\n\nВыберете класс вашего персонажа:",  reply_markup=classes_keyboard)
    await state.set_state(Form.auto_char_class)

@router.callback_query(Form.auto_char_class)
async def enter_char_class(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню с выбором расы персонажа"""
    await callback_query.answer()
    if callback_query.data == 'char_back':
        await state.clear()
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)
    else:
        await state.update_data({"character_class": callback_query.data})
        await callback_query.message.edit_caption(caption="Выберете расу вашего персонажа:",reply_markup=races_keyboard)
        await state.set_state(Form.auto_char_race)

@router.callback_query(Form.auto_char_race)
async def enter_char_race(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню с выбором пола персонажа"""
    await callback_query.answer()
    if callback_query.data == 'char_back':
        await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\n\nВыберете класс вашего персонажа:",  reply_markup=classes_keyboard)
        await state.set_state(Form.auto_char_class)
    else:
        await state.update_data({"race": callback_query.data})
        await callback_query.message.edit_caption(caption="Выберете пол вашего персонажа:",reply_markup=gender_keyboard)
        await state.set_state(Form.auto_char_gender)

@router.callback_query(Form.auto_char_gender)
async def enter_char_gender(callback_query: types.CallbackQuery, state: FSMContext):
    """Создание и вывод автоматически сгенерированного персонажа"""
    await callback_query.answer()
    if callback_query.data == 'char_back':
        await callback_query.message.edit_caption(caption="Выберете расу вашего персонажа:",reply_markup=races_keyboard)
        await state.set_state(Form.auto_char_race)
    else:
        gender = callback_query.data
        await state.update_data({"gender": gender})
        data = await state.get_data()
        response = await auto_create_char({"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]})
        response["user_id"] = str(callback_query.from_user.id)
        char  = await create_char(response)
        await callback_query.message.delete()
        await callback_query.message.answer(text=character_card(response)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)
        await state.update_data({"char": char})
        await state.update_data({"base_char_info" : {"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]}})
    
@router.callback_query(lambda c: c.data == 'discard_character')
async def discard_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие подтверждения удаления персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы действительно хотите удалить персонажа?", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.discard_character)
    
@router.callback_query(Form.discard_character)
async def discard_character(callback_query: types.CallbackQuery, state: FSMContext):
    """Удаление или отмена удаления персонажа"""
    await callback_query.answer()
    if callback_query.data == 'yes':
        await callback_query.message.delete()
        await main_menu(callback_query.message,text="Вы жестоко удалили вашего персонажа!")
    else:
        char = await state.get_data()
        base_info = char["base_char_info"]
        char = char["char"]
        await state.update_data({"base_char_info" : base_info})
        await state.update_data({"char" : char})
        await callback_query.message.delete()
        await callback_query.message.answer(text=f"{character_card(char)["main_char_info"]}\n\nВы отменили удаление персонажа",reply_markup=character_card_keyboard,parse_mode="MarkdownV2")
