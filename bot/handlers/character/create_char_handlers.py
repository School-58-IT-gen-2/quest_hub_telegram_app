from aiogram import types, Router
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests.character_requests import *
from forms import Form
from converter import *


router = Router()

@router.callback_query(Form.regenerate_char)
async def regenerate_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Перегенерация персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == "yes":
        response = await auto_create_char({"gender": char["gender"], "race": char["race"], "character_class": char["character_class"]})
        response["user_id"] = str(callback_query.from_user.id)
        response["name"] = char["name"]
        response["surname"] = char["surname"]
        char = await update_char(response, char["id"])
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
    char = (await state.get_data())["char"]
    if callback_query.data == "yes":
        await delete_char(char["id"])
        await state.clear()
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)
        await callback_query.message.edit_caption(caption="Вы жестоко удалили вашего персонажа!", reply_markup=characters_keyboard)
    if callback_query.data == "no":
        await callback_query.message.edit_text(parse_mode="MarkdownV2",text=f"{(await character_card(char))["main_char_info"]}",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)

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
    char = await state.get_data()
    char_id = char["char"]["id"]
    if callback_query.data == 'yes':
        await delete_char(char_id)
        await callback_query.message.delete()
        await state.clear()
        await callback_query.message.answer_photo(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard, caption="Вы жестоко удалили вашего персонажа!")
    else:
        char = await state.get_data()
        base_info = char["base_char_info"]
        char = char["char"]
        await state.update_data({"base_char_info" : base_info})
        await state.update_data({"char" : char})
        await callback_query.message.delete()
        await state.set_state(Form.main_char_info_menu)
        await callback_query.message.answer(text=f"{(await character_card(char))["main_char_info"]}",reply_markup=character_card_keyboard,parse_mode="MarkdownV2")
