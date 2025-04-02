from aiogram import types, Router
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests.character_requests import *
from forms import Form
from converter import *


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
    char = (await state.get_data())["char"]
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