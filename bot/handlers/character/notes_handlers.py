from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests.character_requests import *
from server_requests.character_requests.notes_requests import *
from forms import Form
from converter import *


router = Router()

@router.callback_query(Form.notes_menu)
async def notes_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заметки персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
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
    title = data["note_title"]
    note = {"title": title, "text": text}
    note = await add_note(char["id"], note)
    char = await get_char(char["id"])
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
    item_id = data["item_id"]
    if callback_query.data == 'yes':
        await delete_note(char["id"], item_id)
        char = await get_char(char["id"])
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