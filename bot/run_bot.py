import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.handlers import CallbackQueryHandler, InlineQueryHandler
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from pathlib import Path

from keyboards import *
from requests import *
from forms import Form


load_dotenv()
logging.basicConfig(level=logging.INFO)


bot = Bot(token=os.getenv("BOT_TOKEN")) # при пул реквесте в development/main поменять на PRODUCTION_BOT_TOKEN
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
    message_text = f"Добро пожаловать, {message.from_user.first_name}!\nБолее известный на ДнД поле как {message.from_user.username}."
    
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

@router.callback_query(lambda c: c.data == 'arrange_meeting')
async def arrange_meeting(callback_query: types.CallbackQuery):
    pass
    # await callback_query.answer()
    # await callback_query.message.edit_text(text="Тут назначение сессии!", reply_markup=session_menu_keyboard)

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
        await callback_query.message.edit_caption(caption="Ваш аккаунт был успешно удален") # логику прикрутить
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
async def auto_create(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=classes_keyboard)
    # etc

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())