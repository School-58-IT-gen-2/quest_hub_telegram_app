from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests import *
from forms import Form
from converter import *


router = Router()

@router.callback_query(Form.traits_menu)
async def traits_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Особенности персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
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
    trait_name = data["trait_name"]
    trait = {"name": trait_name, "description": description}
    trait = await add_trait(char["id"], trait)
    char = await get_char(char["id"])
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
    item_id = data["item_id"]
    if callback_query.data == 'yes':
        await delete_trait(char["id"], item_id)
        char = await get_char(char["id"])
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
    item = await get_trait(char_id, item_id)
    item["name"] = message.text
    item = await update_trait(char_id, item)
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
    item = await get_trait(char_id, item_id)
    item["description"] = message.text
    item = await update_trait(char_id, item)
    char = await get_char(char_id)
    char = char[0]
    await state.update_data({"char": char})
    await state.set_state(Form.trait_menu)
    await message.answer(text=(await character_card(char))["traits_and_abilities"][item_id], reply_markup=trait_keyboard, parse_mode="MarkdownV2")
