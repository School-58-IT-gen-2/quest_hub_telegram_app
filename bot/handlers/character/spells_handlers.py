from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests import *
from forms import Form
from converter import *


router = Router()

@router.callback_query(Form.spells_menu)
async def spells_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Заклинания персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)