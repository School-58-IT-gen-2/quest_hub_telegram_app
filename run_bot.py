import asyncio
import logging
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters.command import Command
from dotenv import load_dotenv
import os
load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    main_keyboard = [
        [types.KeyboardButton(text="Создание персонажа"),types.KeyboardButton(text="Просмотр моих персонажей")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=main_keyboard) # дописать регистрацию
    await message.answer("Приветствуем вас!",reply_markup=keyboard)

@dp.message(F.text == "Создание персонажа")
async def create_char(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb) 
    await message.answer("Тут создание персонажа!",reply_markup=keyboard)

@dp.message(F.text == "Просмотр моих персонажей")
async def create_char(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb) 
    await message.answer("Тут просмотр персонажей!",reply_markup=keyboard)

@dp.message(F.text == "Помощь")
async def create_char(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb) 
    await message.answer("Тут помощь (возможно)!",reply_markup=keyboard)

@dp.message(F.text == "Главная страница")
async def create_char(message: types.Message):
    main_keyboard = [
        [types.KeyboardButton(text="Создание персонажа"),types.KeyboardButton(text="Просмотр моих персонажей")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=main_keyboard) # дописать регистрацию
    await message.answer("Вы на главной странице!",reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())