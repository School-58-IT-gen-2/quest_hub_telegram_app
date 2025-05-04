from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests.character_requests import *
from server_requests.character_requests.main_info_requests import *
from forms import Form
from converter import *


router = Router()

@router.callback_query(Form.main_char_info_menu)
async def main_char_info_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Основные сведения о персонаже"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
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

@router.callback_query(Form.lvl_menu)
async def lvl_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Уровень персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.name_menu)
async def name_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Имя персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
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
    char = (await state.get_data())["char"]
    name = message.text
    await update_name(char["id"], name)
    char["name"] = name
    await state.update_data({"char": char})
    await state.set_state(Form.name_menu)
    await message.answer(text=(await character_card(char))["name"], reply_markup=name_keyboard, parse_mode="MarkdownV2")

@router.message(Form.change_char_surname)
async def change_char_surname(message: types.Message, state: FSMContext):
    """Изменение фамилии персонажа"""
    char = (await state.get_data())["char"]
    surname = message.text
    await update_surname(char["id"], surname)
    char["surname"] = surname
    await state.update_data({"char": char})
    await state.set_state(Form.name_menu)
    await message.answer(text=(await character_card(char))["name"], reply_markup=name_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.age_menu)
async def age_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Возраст персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)
    elif callback_query.data == 'edit':
        await callback_query.message.edit_text(text=f'{(await character_card(char))["age"]}\n\nВведите новый возраст персонажа:',parse_mode="MarkdownV2")
        await state.set_state(Form.change_char_age)

@router.message(Form.change_char_age)
async def change_char_age(message: types.Message, state: FSMContext):
    """Изменение возраста персонажа"""
    char = (await state.get_data())["char"]
    age = message.text
    if age.isdigit():
        if int(age) == 0:
            await message.answer(text="Ждём вашего персонажа через 9 месяцев\!\n\nПожалуйста, введите корректный возраст\.",parse_mode="MarkdownV2")
        else:
            age = int(age)
            await update_age(char["id"], age)
            char["age"] = age
            await state.update_data({"char": char})
            await state.set_state(Form.age_menu)
            await message.answer(text=(await character_card(char))["age"], reply_markup=edit_keyboard, parse_mode="MarkdownV2")
    else:
        await message.answer(text=f"{await tg_text_convert("Тестировщик заходит в бар и заказывает: кружку пива, 2 кружки пива, 0 кружек пива, 999999999 кружек пива, ящерицу в стакане, –1 кружку пива, qwertyuip кружек пива.\n\nПервый реальный клиент заходит в бар и спрашивает, где туалет. Бар вспыхивает пламенем, все погибают.")}\n\nПожалуйста, введите корректный возраст\.",parse_mode="MarkdownV2")

@router.callback_query(Form.languages_menu)
async def languages_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Языки персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
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
    item_id = data["item_id"]
    if callback_query.data == "back":
        await callback_query.message.edit_text(text='🗣️ *_Языки:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить язык", callback_data="add_language")]] + (await build_arr_keyboard((await character_card(char))["languages"]))),parse_mode="MarkdownV2")
        await state.set_state(Form.languages_menu)
    elif callback_query.data == "delete_language":
        await delete_language(char["id"], item_id)
        char = (await get_char(char["id"]))[0]
        await state.update_data({"char": char})
        await callback_query.message.edit_text(text='🗣️ *_Языки:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить язык", callback_data="add_language")]] + (await build_arr_keyboard((await character_card(char))["languages"]))),parse_mode="MarkdownV2")
        await state.set_state(Form.languages_menu)

@router.message(Form.add_language)
async def create_language(message: types.Message, state: FSMContext):
    """Добавление языка"""
    language = message.text
    char = (await state.get_data())["char"]
    await add_language(char["id"], language)
    char = await get_char(char["id"])
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.language_menu)
    await state.update_data({"item_id": language})
    await message.answer(text=f'*_{language}_*', reply_markup=language_keyboard, parse_mode="MarkdownV2")

@router.callback_query(Form.backstory_menu)
async def backstory_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предыстория персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)
    if callback_query.data == 'edit':
        await callback_query.message.edit_text(text=f'{(await character_card(char))["backstory"]}\n\n\nВведите новую предысторию персонажа:',parse_mode="MarkdownV2")
        await state.set_state(Form.change_backstory)
    
@router.message(Form.change_backstory)
async def change_backstory(message: types.Message, state: FSMContext):
    """Изменение предыстории персонажа"""
    char = (await state.get_data())["char"]
    backstory = message.text
    await update_backstory(char["id"], backstory)
    char["backstory"] = backstory
    await state.update_data({"char": char})
    await state.set_state(Form.backstory_menu)
    await message.answer(text=(await character_card(char))["backstory"], reply_markup=edit_keyboard, parse_mode="MarkdownV2")