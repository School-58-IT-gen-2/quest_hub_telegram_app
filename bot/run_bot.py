import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.handlers import CallbackQueryHandler, InlineQueryHandler
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv
from keyboards import *
from requests import *
import os


load_dotenv()
logging.basicConfig(level=logging.INFO)


bot = Bot(token=os.getenv("TEST_BOT_TOKEN")) # при пул реквесте в development/main поменять на PRODUCTION_BOT_TOKEN
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

@router.message()
async def main_menu(message: types.Message):
    await message.answer_photo(photo='https://armorclass.co/cdn/shop/articles/Boels_The_Magic_of_DD_How_Dungeons__Dragons_Works_e82dd415-fe67-43f6-b126-df05fd7e29fb.jpg?v=1695410885&width=2048', text="Главное меню", reply_markup=main_menu_keyboard())

@router.callback_query(lambda c: c.data == 'profile') 
async def profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://armorclass.co/cdn/shop/articles/Boels_The_Magic_of_DD_How_Dungeons__Dragons_Works_e82dd415-fe67-43f6-b126-df05fd7e29fb.jpg?v=1695410885&width=2048'), text="Тут профиль!", reply_markup=account_menu_keyboard())

@router.callback_query(lambda c: c.data == 'main_menu')
async def main_menu_query(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://armorclass.co/cdn/shop/articles/Boels_The_Magic_of_DD_How_Dungeons__Dragons_Works_e82dd415-fe67-43f6-b126-df05fd7e29fb.jpg?v=1695410885&width=2048'), text="Главное меню", reply_markup=main_menu_keyboard())

@router.callback_query(lambda c: c.data == 'characters')
async def characters(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://armorclass.co/cdn/shop/articles/Boels_The_Magic_of_DD_How_Dungeons__Dragons_Works_e82dd415-fe67-43f6-b126-df05fd7e29fb.jpg?v=1695410885&width=2048'), text="Тут персонажи!", reply_markup=characters_keyboard())

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

@router.callback_query(lambda c: c.data == 'create_character')
async def choose_creation(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://armorclass.co/cdn/shop/articles/Boels_The_Magic_of_DD_How_Dungeons__Dragons_Works_e82dd415-fe67-43f6-b126-df05fd7e29fb.jpg?v=1695410885&width=2048'), text="Выберете способ создания персонажа", reply_markup=how_to_create_character_keyboard())

@router.callback_query(lambda c: c.data == 'create_by_myself')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://i.redd.it/ogbv27260cm21.jpg'), text="Создание персонажа", reply_markup=char_list_keyboard_1())
    # await callback_query.message.edit_text(text="Создание персонажа", reply_markup=char_list_keyboard_1())

@router.callback_query(lambda c: c.data == 'page_1')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://i.redd.it/ogbv27260cm21.jpg'), text="Создание персонажа", reply_markup=char_list_keyboard_1())
    
@router.callback_query(lambda c: c.data == 'page_2')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://i.redd.it/ogbv27260cm21.jpg'), text="Создание персонажа", reply_markup=char_list_keyboard_2())

@router.callback_query(lambda c: c.data == 'page_3')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://i.redd.it/ogbv27260cm21.jpg'), text="Создание персонажа", reply_markup=char_list_keyboard_3())

@router.callback_query(lambda c: c.data == 'page_4')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://i.redd.it/ogbv27260cm21.jpg'), text="Создание персонажа", reply_markup=char_list_keyboard_4())

@router.callback_query(lambda c: c.data == 'page_5')
async def create_by_myself(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media='https://i.redd.it/ogbv27260cm21.jpg'), text="Создание персонажа", reply_markup=char_list_keyboard_5())


@router.callback_query(lambda c: c.data == 'auto_create')
async def auto_create(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Выберете класс персонажа", reply_markup=classes_keyboard())
    # etc


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())