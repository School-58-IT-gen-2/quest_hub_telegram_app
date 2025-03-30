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
        char_arr = [[f'{char["name"]} {char["surname"]}', str(char["id"])] for char in user_chars]
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(char_arr))))
        await state.set_state(Form.view_character)

@router.callback_query(Form.view_character)
async def view_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Вывод персонажа"""
    await callback_query.answer()
    if 'left' in callback_query.data or 'right' in callback_query.data:
        user_chars = await get_char_by_user_id(callback_query.from_user.id)
        char_arr = [[f'{char["name"]} {char["surname"]}', str(char["id"])] for char in user_chars]
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=(await change_keyboard_page(callback_query.data, char_arr))))
    elif callback_query.data == "dict_kb_back":
        await characters(callback_query, state)
    else:
        char = (await get_char(callback_query.data))[0]
        await callback_query.message.delete()
        await callback_query.message.answer(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
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
        notes_arr = []
        if char["notes"]:
            notes_arr = [[note["title"], note["id"]] for note in char["notes"]]
        await callback_query.message.edit_text(text='✏️ *_Заметки:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Создать заметку", callback_data="create_note")]] + (await build_arr_keyboard(notes_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.notes_menu)
    if callback_query.data == "traits":
        traits_arr = []
        if char["traits_and_abilities"]:
            traits_arr = [[trait["name"], trait["id"]] for trait in char["traits_and_abilities"]]
        await callback_query.message.edit_text(text='🧬 *_Черты и способности:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить черту / способность", callback_data="create_trait")]] + (await build_arr_keyboard(traits_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.traits_menu)
    if callback_query.data == "main_char_info":
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)
    if callback_query.data == "lvl":
        await callback_query.message.edit_text(text=f'*_Текущий уровень:_* {char['lvl'] if char['lvl'] else 1}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.lvl_menu)
    if callback_query.data == "spells":
        await callback_query.message.edit_text(text='🪄 *_Заклинания:_*\n' + (await character_card(char))["spells"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.spells_menu)
    if callback_query.data == 'delete_character':
        await callback_query.message.edit_text(text="Удалённого персонажа *невозможно восстановить*\. Продолжить\?", reply_markup=yes_or_no_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.delete_character_confirm)
    if callback_query.data == 'regenerate_character_from_put':
        await callback_query.message.edit_text(text="Весь текущий *прогресс персонажа будет утерян*\. Продолжить\?", reply_markup=yes_or_no_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.regenerate_char)

@router.callback_query(Form.notes_menu)
async def notes_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заметки персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        notes_arr = []
        if char["notes"]:
            notes_arr = [[note["title"], note["id"]] for note in char["notes"]]
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Создать заметку", callback_data="create_note")]] + (await change_keyboard_page(callback_query.data, notes_arr))))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)
    elif callback_query.data == "create_note":
        await callback_query.message.edit_text(text="Введите название новой заметки:")
        await state.set_state(Form.create_note_title)
    else:
        await state.set_state(Form.note_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=(await character_card(char))["notes"][callback_query.data], reply_markup=note_keyboard, parse_mode="MarkdownV2")

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
    await message.answer(text=(await character_card(char))["notes"][note["id"]], reply_markup=note_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.note_menu)
async def note_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заметка персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        notes_arr = []
        if char["notes"]:
            notes_arr = [[note["title"], note["id"]] for note in char["notes"]]
        await callback_query.message.edit_text(text='✏️ *_Заметки:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Создать заметку", callback_data="create_note")]] + (await build_arr_keyboard(notes_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.notes_menu)
    elif callback_query.data == "change_title":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["notes"][item_id]}\n\nВведите новое название:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_note_title)
    elif callback_query.data == "change_text":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["notes"][item_id]}\n\nВведите новое содержание:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_note_text)
    elif callback_query.data == "delete_note":
        await callback_query.message.edit_text(text=f'Удалённую заметку *невозможно восстановить*\. Продолжить\?', reply_markup=yes_or_no_keyboard, parse_mode="MarkdownV2")
        await state.set_state(Form.delete_note)

@router.callback_query(Form.delete_note)
async def discard_note(callback_query: types.CallbackQuery, state: FSMContext):
    """Удаление или отмена удаления заметки"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    item_id = data["item_id"]
    if callback_query.data == 'yes':
        await delete_note(char_id, item_id)
        char = await get_char(char_id)
        char = char[0]
        await state.update_data({"char": char})
        notes_arr = []
        if char["notes"]:
            notes_arr = [[note["title"], note["id"]] for note in char["notes"]]
        await callback_query.message.edit_text(text='✏️ *_Заметки:_*\n\nВы удалили вашу заметку\.', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Создать заметку", callback_data="create_note")]] + (await build_arr_keyboard(notes_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.notes_menu)
    else:
        await callback_query.message.edit_text(text=(await character_card(char))["notes"][item_id], reply_markup=note_keyboard, parse_mode="MarkdownV2")
        await state.set_state(Form.note_menu)

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
    await state.set_state(Form.note_menu)
    await message.answer(text=(await character_card(char))["notes"][item_id], reply_markup=note_keyboard, parse_mode="MarkdownV2")

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
    await state.set_state(Form.note_menu)
    await message.answer(text=(await character_card(char))["notes"][item_id], reply_markup=note_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.traits_menu)
async def traits_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Особенности персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        traits_arr = []
        if char["traits_and_abilities"]:
            traits_arr = [[trait["name"], trait["id"]] for trait in char["traits_and_abilities"]]
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить черту / способность", callback_data="create_trait")]] + (await change_keyboard_page(callback_query.data, traits_arr))))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)
    elif callback_query.data == "create_trait":
        await callback_query.message.edit_text(text="Введите название особенности персонажа:")
        await state.set_state(Form.create_trait_name)
    else:
        await state.set_state(Form.trait_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=(await character_card(char))["traits_and_abilities"][callback_query.data], reply_markup=trait_keyboard, parse_mode="MarkdownV2")

@router.message(Form.create_trait_name)
async def create_trait_name(message: types.Message, state: FSMContext):
    """Создание особенности персонажа"""
    trait_name = message.text
    await state.update_data({"trait_name": trait_name})
    await message.answer(text="Введите описание особенности персонажа:")
    await state.set_state(Form.create_trait_description)

@router.message(Form.create_trait_description)
async def create_trait_description(message: types.Message, state: FSMContext):
    """Создание особенности персонажа"""
    description = message.text
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    trait_name = data["trait_name"]
    trait = {"name": trait_name, "description": description}
    trait = await add_ability(char_id, trait)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.trait_menu)
    await state.update_data({"item_id": trait["id"]})
    await message.answer(text=(await character_card(char))["traits_and_abilities"][trait["id"]], reply_markup=trait_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.trait_menu)
async def trait_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Особенность персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        traits_arr = []
        if char["traits_and_abilities"]:
            traits_arr = [[trait["name"], trait["id"]] for trait in char["traits_and_abilities"]]
        await callback_query.message.edit_text(text='🧬 *_Черты и способности:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить черту / способность", callback_data="create_trait")]] + (await build_arr_keyboard(traits_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.traits_menu)
    elif callback_query.data == "change_name":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["traits_and_abilities"][item_id]}\n\nВведите новое название:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_trait_name)
    elif callback_query.data == "change_description":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["traits_and_abilities"][item_id]}\n\nВведите новое описание:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_trait_description)
    elif callback_query.data == "delete_trait":
        await callback_query.message.edit_text(text=f'Удалённую особенность *невозможно восстановить*\. Продолжить\?', reply_markup=yes_or_no_keyboard, parse_mode="MarkdownV2")
        await state.set_state(Form.delete_trait)

@router.callback_query(Form.delete_trait)
async def discard_trait(callback_query: types.CallbackQuery, state: FSMContext):
    """Удаление или отмена удаления ососбенности"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    item_id = data["item_id"]
    if callback_query.data == 'yes':
        await delete_ability(char_id, item_id)
        char = await get_char(char_id)
        char = char[0]
        await state.update_data({"char": char})
        traits_arr = []
        if char["traits_and_abilities"]:
            traits_arr = [[trait["name"], trait["id"]] for trait in char["traits_and_abilities"]]
        await callback_query.message.edit_text(text='🧬 *_Черты и способности:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить черту / способность", callback_data="create_trait")]] + (await build_arr_keyboard(traits_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.traits_menu)
    else:
        await callback_query.message.edit_text(text=(await character_card(char))["traits_and_abilities"][item_id], reply_markup=trait_keyboard, parse_mode="MarkdownV2")
        await state.set_state(Form.trait_menu)

@router.message(Form.change_trait_name)
async def change_trait_name(message: types.Message, state: FSMContext):
    """Изменение названия особенности"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_ability(char_id, item_id)
    print('====================================')
    print(item)
    print('====================================')
    item["name"] = message.text
    item = await update_ability(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.trait_menu)
    await message.answer(text=(await character_card(char))["traits_and_abilities"][item_id], reply_markup=trait_keyboard, parse_mode="MarkdownV2")

@router.message(Form.change_trait_description)
async def change_trait_description(message: types.Message, state: FSMContext):
    """Изменение описания особенности"""
    data = await state.get_data()
    item_id = data["item_id"]
    char_id = data["char"]["id"]
    item = await get_ability(char_id, item_id)
    item["description"] = message.text
    item = await update_ability(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.trait_menu)
    await message.answer(text=(await character_card(char))["traits_and_abilities"][item_id], reply_markup=trait_menu, parse_mode="MarkdownV2")

@router.callback_query(Form.main_char_info_menu)
async def main_char_info_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Основные сведения о персонаже"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "name":
        await callback_query.message.edit_text(text=(await character_card(char))["name"], reply_markup=name_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.name_menu)
    if callback_query.data == "age":
        await callback_query.message.edit_text(text=(await character_card(char))["age"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.age_menu)
    if callback_query.data == "backstory":
        await callback_query.message.edit_text(text=(await character_card(char))["backstory"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.backstory_menu)
    if callback_query.data == "languages":
        await callback_query.message.edit_text(text='🗣️ *_Языки:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить язык", callback_data="add_language")]] + (await build_arr_keyboard((await character_card(char))["languages"]))),parse_mode="MarkdownV2")
        await state.set_state(Form.languages_menu)
    if callback_query.data == "back":
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.spells_menu)
async def spells_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заклинания персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.lvl_menu)
async def lvl_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Уровень персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
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
    elif callback_query.data == 'change_name':
        await callback_query.message.edit_text(text=f'{(await character_card(char))["name"]}\n\nВведите новое имя персонажа:',parse_mode="MarkdownV2")
        await state.set_state(Form.change_char_name)
    elif callback_query.data == 'change_surname':
        await callback_query.message.edit_text(text=f'{(await character_card(char))["name"]}\n\nВведите новую фамилию персонажа:',parse_mode="MarkdownV2")
        await state.set_state(Form.change_char_surname)

@router.message(Form.change_char_name)
async def change_char_name(message: types.Message, state: FSMContext):
    """Изменение имени персонажа"""
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    name = message.text
    await update_name(char_id, name)
    char["name"] = name
    await state.update_data({"char": char})
    await state.set_state(Form.name_menu)
    await message.answer(text=(await character_card(char))["name"], reply_markup=name_keyboard, parse_mode="MarkdownV2")

@router.message(Form.change_char_surname)
async def change_char_surname(message: types.Message, state: FSMContext):
    """Изменение фамилии персонажа"""
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    surname = message.text
    await update_surname(char_id, surname)
    char["surname"] = surname
    await state.update_data({"char": char})
    await state.set_state(Form.name_menu)
    await message.answer(text=(await character_card(char))["name"], reply_markup=name_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.age_menu)
async def age_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Возраст персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)
    elif callback_query.data == 'edit':
        await callback_query.message.edit_text(text=f'{(await character_card(char))["age"]}\n\nВведите новый возраст персонажа:',parse_mode="MarkdownV2")
        await state.set_state(Form.change_char_age)

@router.message(Form.change_char_age)
async def change_char_age(message: types.Message, state: FSMContext):
    """Изменение возраста персонажа"""
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    age = message.text
    if age.isdigit():
        if int(age) == 0:
            await message.answer(text="Ждём вашего персонажа через 9 месяцев\!\n\nПожалуйста введите корректный возраст\.",parse_mode="MarkdownV2")
        else:
            age = int(age)
            await update_age(char_id, age)
            char["age"] = age
            await state.update_data({"char": char})
            await state.set_state(Form.age_menu)
            await message.answer(text=(await character_card(char))["age"], reply_markup=edit_keyboard, parse_mode="MarkdownV2")
    else:
        await message.answer(text=f"{await tg_text_convert("Тестировщик заходит в бар и заказывает: кружку пива, 2 кружки пива, 0 кружек пива, 999999999 кружек пива, ящерицу в стакане, –1 кружку пива, qwertyuip кружек пива.\n\nПервый реальный клиент заходит в бар и спрашивает, где туалет. Бар вспыхивает пламенем, все погибают.")}\n\nПожалуйста введите корректный возраст\.",parse_mode="MarkdownV2")

@router.callback_query(Form.backstory_menu)
async def backstory_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предыстория персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)
    elif callback_query.data == 'edit':
        await callback_query.message.edit_text(text=f'{(await character_card(char))["backstory"]}\n\n\nВведите новую предысторию персонажа:',parse_mode="MarkdownV2")
        await state.set_state(Form.change_backstory)
    
@router.message(Form.change_backstory)
async def change_backstory(message: types.Message, state: FSMContext):
    """Изменение предыстории персонажа"""
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    backstory = message.text
    await update_backstory(char_id, backstory)
    char["backstory"] = backstory
    await state.update_data({"char": char})
    await state.set_state(Form.backstory_menu)
    await message.answer(text=(await character_card(char))["backstory"], reply_markup=edit_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.languages_menu)
async def languages_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Языки персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить язык", callback_data="add_language")]] + (await change_keyboard_page(callback_query.data, (await character_card(char)["languages"])))))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)
    elif callback_query.data == "add_language":
        await callback_query.message.edit_text(text="Введите название нового языка:")
        await state.set_state(Form.add_language)
    else:
        await state.set_state(Form.language_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=f'*_{callback_query.data}_*', reply_markup=language_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.language_menu)
async def language_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Язык персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        await callback_query.message.edit_text(text='🗣️ *_Языки:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить язык", callback_data="add_language")]] + (await build_arr_keyboard((await character_card(char))["languages"]))),parse_mode="MarkdownV2")
        await state.set_state(Form.languages_menu)
    elif callback_query.data == "delete_language":
        await delete_language(char_id, item_id)
        char = (await get_char(char_id))[0]
        await state.update_data({"char": char})
        await callback_query.message.edit_text(text='🗣️ *_Языки:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить язык", callback_data="add_language")]] + (await build_arr_keyboard((await character_card(char))["languages"]))),parse_mode="MarkdownV2")
        await state.set_state(Form.languages_menu)

@router.message(Form.add_language)
async def create_language(message: types.Message, state: FSMContext):
    """Добавление языка"""
    language = message.text
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    await add_language(char_id, language)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.language_menu)
    await state.update_data({"item_id": language})
    await message.answer(text=f'*_{language}_*', reply_markup=language_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.inventory_menu)
async def inventory(callback_query: types.CallbackQuery, state: FSMContext):
    """Инвентарь персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "items":
        items_arr = [[item["name"], item["id"]] for item in char["inventory"]]
        await callback_query.message.edit_text(text=f'🛠️ *_Снаряжение:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(items_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.items_menu)
    if callback_query.data == "ammunition":
        ammunition_arr = [[weapon["name"], weapon["id"]] for weapon in char["weapons_and_equipment"]]
        await callback_query.message.edit_text(text=f'🛡️ *_Амуниция:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(ammunition_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.ammunition_menu)
    if callback_query.data == "exp":
        await callback_query.message.edit_text(text=f'*_Текущий опыт:_* {char['experience']}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.experience_menu)
    if callback_query.data == "gold":
        await callback_query.message.edit_text(text=f'*_Текущее количество золота:_* {char['gold']}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.gold_menu)
    if callback_query.data == "back":
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.items_menu)
async def items_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Снаряжение персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        items_arr = [[item["name"], item["id"]] for item in char["inventory"]]
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=(await change_keyboard_page(callback_query.data, items_arr))))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text='📋 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await state.set_state(Form.inventory_item_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=(await character_card(char))["inventory"][callback_query.data], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.inventory_item_menu)
async def inventory_item_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предмет персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        items_arr = [[item["name"], item["id"]] for item in char["inventory"]]
        await callback_query.message.edit_text(text=f'🛠️ *_Снаряжение:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(items_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.items_menu)
    elif callback_query.data == "change_name":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["inventory"][item_id]}\n\nВведите новое название:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_inventory_item_name)
    elif callback_query.data == "change_desc":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["inventory"][item_id]}\n\nВведите новое описание:', parse_mode="MarkdownV2")
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
    await message.answer(text=(await character_card(char))["inventory"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

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
    await message.answer(text=(await character_card(char))["inventory"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.gold_menu)
async def gold_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Золото персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='📋 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
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
        ammunition_arr = [[weapon["name"], weapon["id"]] for weapon in char["weapons_and_equipment"]]
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=(await change_keyboard_page(callback_query.data, ammunition_arr))))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text='📋 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await state.set_state(Form.ammunition_item_menu)
        await state.update_data({"item_id": callback_query.data})
        await callback_query.message.edit_text(text=(await character_card(char))["ammunition"][callback_query.data], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.ammunition_item_menu)
async def ammunition_item_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предмет персонажа"""
    await callback_query.answer()
    data = await state.get_data()
    char = data["char"]
    item_id = data["item_id"]
    if callback_query.data == "back":
        ammunition_arr = [[weapon["name"], weapon["id"]] for weapon in char["weapons_and_equipment"]]
        await callback_query.message.edit_text(text=f'🛡️ *_Амуниция:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(ammunition_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.ammunition_menu)
    elif callback_query.data == "change_name":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["ammunition"][item_id]}\n\nВведите новое название:', parse_mode="MarkdownV2")
        await state.set_state(Form.change_ammunition_item_name)
    elif callback_query.data == "change_desc":
        await callback_query.message.edit_text(text=f'{(await character_card(char))["ammunition"][item_id]}\n\nВведите новое описание:', parse_mode="MarkdownV2")
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
    await message.answer(text=(await character_card(char))["ammunition"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

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
    await message.answer(text=(await character_card(char))["ammunition"][item_id], reply_markup=item_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.experience_menu)
async def experience_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Опыт персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='📋 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
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
    data = await state.get_data()
    char = data["char"]
    char_id = char["id"]
    if callback_query.data == "yes":
        response = await auto_create_char({"gender": char["gender"], "race": char["race"], "character_class": char["character_class"]})
        response["user_id"] = str(callback_query.from_user.id)
        response["name"] = char["name"]
        response["surname"] = char["surname"]
        char = await update_char(response, char_id)
        await state.update_data({"char": char})
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)
    else:
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
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
        await callback_query.message.edit_text(parse_mode="MarkdownV2",text=f"{(await character_card(char))["main_char_info"]}",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)

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
    await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\n\nВыберите класс вашего персонажа:",  reply_markup=classes_keyboard)
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
        await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\n\nВыберите класс вашего персонажа:",  reply_markup=classes_keyboard)
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
        await callback_query.message.answer(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)
        await state.update_data({"char": char})
        await state.update_data({"base_char_info" : {"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]}})
    
@router.callback_query(lambda c: c.data == 'discard_character')
async def discard_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие подтверждения удаления персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_text(text="Удалённого персонажа *невозможно восстановить*\. Продолжить\?", reply_markup=yes_or_no_keyboard,parse_mode="MarkdownV2")
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
        await callback_query.message.answer(text=f"{(await character_card(char))["main_char_info"]}",reply_markup=character_card_keyboard,parse_mode="MarkdownV2")
