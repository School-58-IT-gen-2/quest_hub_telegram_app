from aiogram import Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InputMediaPhoto

from keyboards.common_keyboards import *
from server_requests.profile_requests import *


dp = Dispatcher()
router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    """Вывод приветствия и создание пользователя"""
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
    await message.answer_photo(caption=message_text,photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard)

@router.message(Command("help"))
async def help(message: types.Message):
    """Вывод помощи"""
    await message.answer("Тут помощь (возможно)!")

@router.callback_query(lambda c: c.data == 'main_menu')
async def main_menu_query(callback_query: types.CallbackQuery):
    """Вывод главного меню (редактирование сообщения)"""
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/main_menu.png")), reply_markup=main_menu_keyboard)

async def main_menu(message: types.Message, text: str = ""):
    """Вывод главного меню (отправка нового сообщения)"""
    await message.answer_photo(caption=text,photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard)
