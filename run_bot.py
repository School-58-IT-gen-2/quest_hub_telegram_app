import asyncio
import logging
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from dotenv import load_dotenv
import os
import json
import httpx
load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()



class Form(StatesGroup):
    gender = State()
    rac = State()
    clas = State()



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
            "is_bot": message.from_user.is_bot,
            "language_code": message.from_user.language_code,
            "is_premium": False,
            "username": message.from_user.username,
            "age": 52,
            "tg_id": message.from_user.id
        }
    
    message_text = f"Добро пожаловать, {message.from_user.first_name}!\nБолее известный на ДнД поле как {message.from_user.username}."
    user = httpx.get(url="http://localhost:9009/api/v1/auth/sign-in",params={"tg_id": message.from_user.id,"first_name": message.from_user.first_name})
    await message.answer(message_text,reply_markup=keyboard)

@dp.message(F.text == "Создание персонажа")
async def create_char(message: types.Message):
    kb_races = [
        [types.KeyboardButton(text="Человек"),types.KeyboardButton(text="Эльф"),types.KeyboardButton(text="Гном"),types.KeyboardButton(text="Полуэльф"),types.KeyboardButton(text="Полурослик"),types.KeyboardButton(text="Гоблин"),types.KeyboardButton(text="Орк")],
        [types.KeyboardButton(text="Назад")]
    ]
    kb_classes = [[types.KeyboardButton(text="Воин"),types.KeyboardButton(text="Маг"),types.KeyboardButton(text="Вор"),types.KeyboardButton(text="Друид"),types.KeyboardButton(text="Паладин")],
                [types.KeyboardButton(text="Назад")]]
    kb = [[types.KeyboardButton(text="Создать самому"),types.KeyboardButton(text="Пройти тест")],
            [types.KeyboardButton(text="Главная страница")]]


    @dp.message(F.text == "Создать самому") # тут бует много страничек, так что пока скип
    async def no_test_creation(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_races,resize_keyboard=True,input_field_placeholder="Выбери расу!")
        await message.answer("Выбери расу!",reply_markup=keyboard)
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_classes,resize_keyboard=True,input_field_placeholder="Выбери расу!")
        await message.answer("Выбери Класс!",reply_markup=keyboard)

    @dp.message(F.text == "Пройти тест")
    async def with_test_creation(message: types.Message):
        user_data = {'gender':None,'rac':None,'clas':None}
        await message.answer("""Для генерации персонажа, пожалуйста, ответьте на три вопроса (напишите все в одном сообщении через пробел)\n\nПервый вопрос: вы хотите персонажа мужского или женского пола? (напишите просто М или Ж)\n\nВторой вопрос: выберите расу персонажа (напишите только название расы с большой буквы, например Дварф)\n\nТретий вопрос: выберите класс персонажа (напишите только название класса с большой буквы, например Воин)""")

        @dp.message(F.text != "Пройти тест")
        async def get_data(message: types.Message):
            s = message.text.split(" ")
            user_data['gender'] = s[0]
            user_data['rac'] = s[1]
            user_data['clas'] = s[2]   
            try:
                user = httpx.post(url="http://localhost:8000/register/",params=user_data)
                print(user.json())
                await message.answer(f"Вы успешно создали персонажа!")
            except:
                await message.answer("Ошибка при создании персонажа!")
    
    @dp.message(F.text == "Назад")
    async def back(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="И вот вы снова у начала...")
        await message.answer("Вы вернулись к началу создания персонажа.",reply_markup=keyboard)

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Тут создание персов X)") 
    await message.answer("Тут создание персонажа!",reply_markup=keyboard)

@dp.message(F.text == "Просмотр моих персонажей")
async def view_chars(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!") 
    await message.answer("Тут просмотр персонажей!",reply_markup=keyboard)

@dp.message(F.text == "Помощь")
async def help(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Тут помощь Х)") 
    await message.answer("Тут помощь (возможно)!",reply_markup=keyboard)

@dp.message(F.text == "Главная страница")
async def mainpage(message: types.Message):
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