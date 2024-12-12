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

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    main_keyboard = [
        [types.KeyboardButton(text="Персонажи"),types.KeyboardButton(text="Профиль")],
        [types.KeyboardButton(text="Помощь"),types.KeyboardButton(text="Назначить сессию")]
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
    """user = httpx.get(url="http://localhost:9009/api/v1/auth/user",params={"tg_id":message.from_user.id}).status_code()
    print(user)"""
    await message.answer(message_text,reply_markup=keyboard)


@dp.message(F.text == "Профиль")
async def view_profile(message: types.Message):
    kb = [[types.KeyboardButton(text="Изменить данные")],[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
    await message.answer("Тут профиль!",reply_markup=keyboard)


    @dp.message(F.text == "Изменить данные")
    async def change_data(message: types.Message):
        kb = [[types.KeyboardButton(text="Изменить возраст")],
              [types.KeyboardButton(text="Главная страница")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Менялка")
        await message.answer("Тут менялка!",reply_markup=keyboard)

        @dp.message(F.text == "Изменить возраст")
        async def change_age(message: types.Message):
            kb = [[types.KeyboardButton(text="Главная страница")]]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Менялка")
            await message.answer("Введите новый возраст",reply_markup=keyboard)
            @dp.message(F.text != "Изменить возраст")
            async def change_age(message: types.Message):
                kb = [[types.KeyboardButton(text="Главная страница")]]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Менялка")
                await message.answer("Вы уцспешно изменили возраст!",reply_markup=keyboard)
                age = int(message.text)
                print(age)


@dp.message(F.text == "Назначить сессию")
async def set_session(message: types.Message):
    kb = [[types.KeyboardButton(text="Назначить новую"),types.KeyboardButton(text="Просмотреть имеющиеся")],
          [types.KeyboardButton(text="Отменить сессию")],
          [types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Сеся")
    await message.answer("Тут назначение сессии!",reply_markup=keyboard)


@dp.message(F.text == "Персонажи")
async def view_chars(message: types.Message):
    kb = [[types.KeyboardButton(text="Просмотреть персонажей"),types.KeyboardButton(text="Создать персонажа")],[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!") 
    await message.answer("Тут просмотр персонажей!",reply_markup=keyboard)

    @dp.message(F.text == "Просмотреть персонажей")
    async def view_chars(message: types.Message):
        char_name = "Бешенный ананас"
        kb = [[types.KeyboardButton(text=char_name)],[types.KeyboardButton(text="Главная страница")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
        await message.answer("Тут просмотр персонажей!",reply_markup=keyboard)


        @dp.message(F.text == char_name)
        async def view_char(message: types.Message):
            kb = [[types.KeyboardButton(text="Изменить"),types.KeyboardButton(text="Удалить")],[types.KeyboardButton(text="Главная страница")]]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
            await message.answer("Тут просмотр персонажа!",reply_markup=keyboard)

            @dp.message(F.text == "Изменить")
            async def change_char(message: types.Message):
                kb = [[types.KeyboardButton(text="Изменить имя"),types.KeyboardButton(text="Изменить класс")],[types.KeyboardButton(text="Главная страница")]] # туь пока базово, потому что много кнопок делать
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
                await message.answer("Выбирете то, что хотите изменить",reply_markup=keyboard)

            @dp.message(F.text == "Удалить")
            async def delete_char(message: types.Message):
                kb = [[types.KeyboardButton(text="Да"),types.KeyboardButton(text="Нет")],[types.KeyboardButton(text="Главная страница")]]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
                await message.answer("Вы уверены?",reply_markup=keyboard)

                @dp.message(F.text == "Да")
                async def delete_char_yes(message: types.Message):
                    kb = [[types.KeyboardButton(text="Главная страница")]]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
                    await message.answer("Персонаж успешно удален!",reply_markup=keyboard)
                
                @dp.message(F.text == "Нет")
                async def delete_char_no(message: types.Message):
                    kb = [
                        [types.KeyboardButton(text="Персонажи"),types.KeyboardButton(text="Профиль")],
                        [types.KeyboardButton(text="Помощь"),types.KeyboardButton(text="Назначить сессию")]
                    ]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
                    await message.answer("Удаление персонажа отменено!",reply_markup=keyboard)



    @dp.message(F.text == "Создать персонажа")
    async def create_char(message: types.Message):
        kb = [[types.KeyboardButton(text="Создать самому"),types.KeyboardButton(text="Пройти тест")],[types.KeyboardButton(text="Главная страница")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
        await message.answer("Тут создание персонажа!",reply_markup=keyboard)
    

    @dp.message(F.text == "Создать самому")
    async def create_char_self(message: types.Message): # пока ничего не писал 
        kb = [[types.KeyboardButton(text="Главная страница")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
        await message.answer("Тут создание персонажа!",reply_markup=keyboard)

    @dp.message(F.text == "Пройти тест")
    async def test(message: types.Message):
        user_data = {"gender":None,"rac":None,"clas":None}
        kb = [[types.KeyboardButton(text="Главная страница")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
        await message.answer("Чтобы пройти тест, Вам нужно ответить на три простых вопроса. Ответы запишите в одну строчку через пробел\n\nКакого пола будет ваш персонаж?(напишите только М или Ж)\n\nКакой расы будет ваш персонаж?(напишите расу с большой буквы, например, Дварф)\n\nКакого класса будет ваш персонаж?(напишите только название класса с большой буквы, например, Воин)",reply_markup=keyboard)
        
        @dp.message(F.text != "Пройти тест") # пока тут костыль
        async def get_data(message: types.Message):
            user_data["gender"] = message.text.split()[0]
            user_data["rac"] = message.text.split()[1]
            user_data["clas"] = message.text.split()[2]
            await message.answer("Отлично! Ваш персонаж создан!",reply_markup=keyboard)


@dp.message(F.text == "Помощь")
async def help(message: types.Message):
    kb = [[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Тут помощь Х)") 
    await message.answer("Тут помощь (возможно)!",reply_markup=keyboard)

@dp.message(F.text == "Главная страница")
async def mainpage(message: types.Message):
    main_keyboard = [
        [types.KeyboardButton(text="Персонажи"),types.KeyboardButton(text="Профиль")],
        [types.KeyboardButton(text="Помощь"),types.KeyboardButton(text="Назначить сессию")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=main_keyboard,resize_keyboard=True,input_field_placeholder="Что же вы выберете?")
    await message.answer("Вы на главной странице!",reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())