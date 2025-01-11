import asyncio
import logging
import os
import json

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.handlers import CallbackQueryHandler, InlineQueryHandler
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from pathlib import Path

from keyboards import *
from requests_to_server import *
from forms import Form


load_dotenv()
logging.basicConfig(level=logging.INFO)


bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    user_data = {
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "role": "player",
            "is_bot": message.from_user.is_bot,
            "language_code": message.from_user.language_code,
            "is_premium": message.from_user.is_premium,
            "username": message.from_user.username,
            "age": 0,
            "tg_id": message.from_user.id
        }    
    message_text = f"Добро пожаловать, {message.from_user.first_name}!\nБолее известный в Фаэруне как {message.from_user.username}."
    await create_user(user_data)
    await message.answer(message_text)
    await main_menu(message)

@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Тут помощь (возможно)!")

async def main_menu(message: types.Message):
    await message.answer_photo(photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard)

@router.callback_query(lambda c: c.data == 'profile') 
async def profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/profile.png")), reply_markup=account_menu_keyboard)

@router.callback_query(lambda c: c.data == 'main_menu')
async def main_menu_query(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/main_menu.png")), reply_markup=main_menu_keyboard)

@router.callback_query(lambda c: c.data == 'characters')
async def characters(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)

@router.callback_query(lambda c: c.data == 'view_characters')
async def view_characters(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    user_chars = await get_char_by_user_id(callback_query.from_user.id)
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=build_char_kb(user_chars))
    await state.set_state(Form.view_character)

@router.callback_query(Form.view_character)
async def view_char(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.clear()
    char = await get_char_by_char_id(int(callback_query.data))
    await callback_query.message.answer(text=f"```\n{json.dumps(char[0],indent=2, ensure_ascii=False)}\n```",parse_mode="Markdown") #придумать красивый вывод

@router.callback_query(lambda c: c.data == 'arrange_meeting')
async def arrange_meeting(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/profile.png")), reply_markup=session_menu_keyboard)

@router.callback_query(lambda c: c.data == 'change_profile')
async def change_profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=change_user_data_keyboard)

@router.callback_query(lambda c: c.data == 'change_age')
async def change_age(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_caption(caption="Введите ваш возраст")
    await state.set_state(Form.get_user_age)

@router.message(Form.get_user_age)
async def set_user_age(message: types.Message, state: FSMContext):
    # Здесь должно записыаться в БД
    await message.answer_photo(photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard, caption=f"Ваш возраст изменен на {message.text}")
    user_data = {
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "role": "player",
            "is_bot": message.from_user.is_bot,
            "language_code": message.from_user.language_code,
            "is_premium": message.from_user.is_premium,
            "username": message.from_user.username,
            "age": int(message.text),
            "tg_id": message.from_user.id
        }
    await update_user(user_data) 
    await state.clear()

@router.callback_query(lambda c: c.data == 'delete_profile')
async def delete_profile(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_caption(caption="Вы действительно хотите удалить профиль?", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.delete_profile_confirm)

@router.callback_query(Form.delete_profile_confirm)
async def confirm_delete_profile(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.clear()
    if callback_query.data == 'yes':
        await delete_user(tg_id = callback_query.from_user.id)
        await callback_query.message.edit_caption(caption="Ваш аккаунт был успешно удален")

    elif callback_query.data == 'no':
        await callback_query.message.edit_caption(caption="Вы отменили удаление аккаунта")
    await asyncio.sleep(1.0)
    await main_menu(callback_query.message)

@router.callback_query(lambda c: c.data == 'create_character')
async def choose_creation(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/char_create.png")))
    await callback_query.message.edit_caption(caption="Выберете способ создания персонажа",  reply_markup=how_to_create_character_keyboard)

@router.callback_query(lambda c: c.data == 'create_by_myself')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=char_list_keyboard_1)

@router.callback_query(lambda c: c.data == 'page_1')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=char_list_keyboard_1)

@router.callback_query(lambda c: c.data == 'gender')
async def write_gender(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=gender_keyboard)
    await state.set_state(Form.enter_char_gender)

@router.callback_query(Form.enter_char_gender)
async def write_gender_in_state(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data({"gender": callback_query.data})
    await callback_query.message.edit_caption(reply_markup=char_list_keyboard_1)
    print(await state.get_data())
    await state.clear() # в такой же форме пишем остальные 28 функций :)

@router.callback_query(lambda c: c.data == 'page_2')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=char_list_keyboard_2)

@router.callback_query(lambda c: c.data == 'page_3')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=char_list_keyboard_3)

@router.callback_query(lambda c: c.data == 'page_4')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=char_list_keyboard_4)

@router.callback_query(lambda c: c.data == 'page_5')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=char_list_keyboard_5)

@router.callback_query(lambda c: c.data == 'auto_create')
async def auto_create(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=classes_keyboard)
    await state.set_state(Form.auto_char_class)

@router.callback_query(Form.auto_char_class)
async def enter_char_class(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data({"clas": callback_query.data})
    await callback_query.message.edit_caption(reply_markup=races_keyboard)
    await state.set_state(Form.auto_char_race)

@router.callback_query(Form.auto_char_race)
async def enter_char_race(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data({"rac": callback_query.data})
    await callback_query.message.edit_caption(reply_markup=gender_keyboard)
    await state.set_state(Form.auto_char_gender)

@router.callback_query(Form.auto_char_gender)
async def enter_char_gender(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data({"gender": callback_query.data})
    response = await auto_create_char(await state.get_data())
    print('==============================')
    print(response)
    print('==============================')
    await callback_query.message.edit_caption(caption=character_info(response), parse_mode="MarkdownV2") 

async def character_info(char_info: dict) -> str:
    print('==============================')
    return (
        f"*_{char_info['name']} {char_info['surname']}_*\n\n"
        f"*_Карточка персонажа:_*\n"
        f"*Раса:* {char_info['race']}"
    )

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())