from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests.character_requests import *
from server_requests.character_requests.inventory_requests import *
from forms import Form
from converter import *


router = Router()

@router.callback_query(Form.inventory_menu)
async def inventory(callback_query: types.CallbackQuery, state: FSMContext):
    """Инвентарь персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == "items":
        items_arr = [[item["name"], item["id"]] for item in char["inventory"]]
        await callback_query.message.edit_text(text=f'🛠️ *_Снаряжение:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(items_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.items_menu)
    if callback_query.data == "ammunition":
        ammunition_arr = [[weapon["name"], weapon["id"]] for weapon in char["weapons_and_equipment"]]
        await callback_query.message.edit_text(text=f'🛡️ *_Амуниция:_*', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(ammunition_arr))),parse_mode="MarkdownV2")
        await state.set_state(Form.ammunition_menu)
    if callback_query.data == "exp":
        await callback_query.message.edit_text(text=f'*_Текущий опыт:_* {char["experience"]}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.experience_menu)
    if callback_query.data == "gold":
        await callback_query.message.edit_text(text=f'*_Текущее количество золота:_* {char["gold"]}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.gold_menu)
    if callback_query.data == "back":
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)

@router.callback_query(Form.items_menu)
async def items_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Снаряжение персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
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
    char = (await state.get_data())["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='📋 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await callback_query.message.edit_text(text=f"*_Текущее количество золота:_* {char['gold']}\n\nВведите количество золота\, которое вы хотите добавить/убрать\. Например `+10` или `-4`\.",parse_mode="MarkdownV2")
        await state.set_state(Form.change_gold)

@router.message(Form.change_gold)
async def change_gold(message: types.Message, state: FSMContext):
    """Изменить количество золота персонажа"""
    char = (await state.get_data())["char"]
    data = message.text
    if check_int(data):
        if char['gold'] + int(data) < 0:
            await message.answer(text="Вы не можете потратить больше золота, чем у вас есть.")
        else:
            await update_gold(char["id"], data)
            char['gold'] += int(data)
            await state.update_data({"char": char})
            await message.answer(text=f'*_Текущее количество золота:_* {char["gold"]}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
            await state.set_state(Form.gold_menu)
    else:
        await message.answer(text="Пожалуйста, используйте корректный формат ввода.")

@router.callback_query(Form.ammunition_menu)
async def ammunition_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Амуниция персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
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
    char = (await state.get_data())["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='📋 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    else:
        await callback_query.message.edit_text(text=f"*_Текущий опыт:_* {char['experience']}\n\nВведите количество опыта\, которое вы хотите добавить/убрать\. Например `+12` или `-3`\.",parse_mode="MarkdownV2")
        await state.set_state(Form.change_xp)

@router.message(Form.change_xp)
async def change_xp(message: types.Message, state: FSMContext):
    """Изменить количество опыта персонажа"""
    char = (await state.get_data())["char"]
    data = message.text
    if check_int(data):
        if char['experience'] + int(data) < 0:
            await message.answer(text="У вас не может быть отрицательное количество опыта.")
        else:
            await update_experience(char["id"], data)
            char['experience'] += int(data)
            await state.update_data({"char": char})
            await message.answer(text=f'*_Текущий опыт:_* {char["experience"]}', reply_markup=edit_keyboard,parse_mode="MarkdownV2")
            await state.set_state(Form.experience_menu)
    else:
        await message.answer(text="Пожалуйста, используйте корректный формат ввода.")