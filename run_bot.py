import asyncio
import logging
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters.command import Command
from dotenv import load_dotenv
import os
import json
import requests
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
    keyboard = types.ReplyKeyboardMarkup(keyboard=main_keyboard,resize_keyboard=True,input_field_placeholder="Велкам аур биутифул юзер, ви а глед ту си ю агейн") 
    user_data = {
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "role": "player",
            "is_bot": False,
            "language_code": "rus",
            "is_premium": False,
            "username": f"super_ultra_{message.from_user.first_name.lower()}_pro",
            "age": 52,
            "tg_id": message.from_user.id
        }
    
    message_text = f"С возвращением, {message.from_user.first_name}!\nБолее известный на ДнД поле как super_ultra_{message.from_user.first_name.lower()}_pro."
    user =  requests.get(url="http://localhost:9009/api/v1/auth/sign-in",params={"tg_id": message.from_user.id,"first_name": message.from_user.first_name})
    print(user)
    if user != []:
        pass
    else:
        register_user = requests.post(url="http://localhost:9009/api/v1/auth/sign-up",params=user_data)
        message_text = f"Приветствуем вас в нашем боте, {message.from_user.first_name}!\nТут вы можете создать персонажей, просмотреть их и многое другое!\nТак как вы новичок, то запишем вас как super_ultra_{message.from_user.first_name.lower()}_pro, надеюсь, вы не против! X)"    
    #ошибка пофикшена X)
    await message.answer(message_text,reply_markup=keyboard)

@dp.message(F.text == "Создание персонажа")
async def create_char(message: types.Message):
    kb_races = [
        [types.KeyboardButton(text="Человек"),types.KeyboardButton(text="Эльф"),types.KeyboardButton(text="Гном"),types.KeyboardButton(text="Полуэльф"),types.KeyboardButton(text="Полурослик"),types.KeyboardButton(text="Гоблин"),types.KeyboardButton(text="Орк")],
        [types.KeyboardButton(text="Назад")]
    ]
    kb_classes = [[types.KeyboardButton(text="Воин"),types.KeyboardButton(text="Маг"),types.KeyboardButton(text="Вор"),types.KeyboardButton(text="Друид"),types.KeyboardButton(text="Паладин")],
                [types.KeyboardButton(text="Назад")]]
    kb = [[types.KeyboardButton(text="Раса")],
            [types.KeyboardButton(text="Класс")],
            [types.KeyboardButton(text="Главная страница")]]


    @dp.message(F.text == "Раса")
    async def races(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_races,resize_keyboard=True,input_field_placeholder="Выбери расу!")
        await message.answer("Выбери расу!",reply_markup=keyboard)

    @dp.message(F.text == "Класс")
    async def races(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_classes,resize_keyboard=True,input_field_placeholder="Выбери расу!")
        await message.answer("Выбери класс!",reply_markup=keyboard)
    
    @dp.message(F.text == "Назад")
    async def races(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="И вот вы снова у начала...")
        await message.answer("Вы вернулись к началу создания персонажа.",reply_markup=keyboard)

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Тут создание персов X)") 
    await message.answer("Тут создание персонажа!",reply_markup=keyboard)

@dp.message(F.text == "Просмотр моих персонажей")
async def create_char(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!") 
    await message.answer("Тут просмотр персонажей!",reply_markup=keyboard)

@dp.message(F.text == "Помощь")
async def create_char(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Тут помощь Х)") 
    await message.answer("Тут помощь (возможно)!",reply_markup=keyboard)

@dp.message(F.text == "Главная страница")
async def create_char(message: types.Message):
    main_keyboard = [
        [types.KeyboardButton(text="Создание персонажа"),types.KeyboardButton(text="Просмотр моих персонажей")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=main_keyboard,resize_keyboard=True,input_field_placeholder="Что же вы выберете?")
    await message.answer("Вы на главной странице!",reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())