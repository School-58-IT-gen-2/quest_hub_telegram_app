import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.handlers import CallbackQueryHandler, InlineQueryHandler
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from all_keyboards import *
import os
import json
import httpx
load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TEST_BOT_TOKEN"))
dp = Dispatcher()
router = Router()




@dp.message(Command("start"))
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
    """user = httpx.get(url="http://localhost:9009/api/v1/auth/user",params={"tg_id":user_data["tg_id"]},headers={"Content-Type": "application/json"})
    if int(user.status_code) == 400:
        user = httpx.post(url="http://localhost:9009/api/v1/auth/user",data=json.dumps(user_data,ensure_ascii=False))
        message_text = "Приветствуем Вас в нашем боте! Ваш аккаунт был успешно создан. Теперь вы можете использовать все возможности нашего бота."""
    await message.answer(message_text)
    await main_menu(message)

@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Тут помощь (возможно)!")

@dp.message()
async def main_menu(message: types.Message):
    kb = main_menu_keyboard()
    await message.answer("Главное меню", reply_markup=main_menu_keyboard())

@router.callback_query(lambda c: c.data == 'profile') #работает только раз и это фиаско!1!!1111111!!!!
async def profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Тут профиль!", reply_markup=account_menu_keyboard())

@router.callback_query(lambda c: c.data == 'main_menu')
async def main_menu_query(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(inline_message_id=callback_query.inline_message_id, text="Главное меню", reply_markup=main_menu_keyboard())

@router.callback_query(lambda c: c.data == 'characters')
async def characters(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Тут персонажи!", reply_markup=characters_keyboard())

@router.callback_query(lambda c: c.data == 'arrange_meeting')
async def arrange_meeting(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Тут назначение сессии!", reply_markup=session_menu_keyboard())

@router.callback_query(lambda c: c.data == 'change_profile')
async def change_profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Выберете параметр, который хотите изменить", reply_markup=change_user_data_keyboard())

@router.callback_query(lambda c: c.data == 'change_age')
async def change_age(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Введите новый возраст")
    #разобраться с вводом возраста

@router.callback_query(lambda c: c.data == 'delete_profile')
async def delete_profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы действительно хотите удалить аккаунт?", reply_markup=yes_or_no_keyboard())
    @router.callback_query(lambda c: c.data == 'yes')
    async def confirm_delete_profile(callback_query: types.CallbackQuery):
        await callback_query.answer()
        await callback_query.message.edit_text(text="Ваш аккаунт был успешно удален") #логику прикрутить
        await asyncio.sleep(1.0)
        await callback_query.message.edit_text(text="Главное меню", reply_markup=main_menu_keyboard())
    @router.callback_query(lambda c: c.data == 'no')
    async def cancel_delete_profile(callback_query: types.CallbackQuery):
        await callback_query.answer()
        await callback_query.message.edit_text(text="Вы отменили удаление аккаунта")
        await asyncio.sleep(1.0)
        await callback_query.message.edit_text(text="Главное меню", reply_markup=main_menu_keyboard())






async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())