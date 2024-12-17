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
            "is_premium": message.from_user.is_premium,
            "username": message.from_user.username,
            "age": 0,
            "tg_id": message.from_user.id
        }    

    message_text = f"Добро пожаловать, {message.from_user.first_name}!\nБолее известный на ДнД поле как {message.from_user.username}."
    user = httpx.get(url="http://localhost:9009/api/v1/auth/user",params={"tg_id":user_data["tg_id"]},headers={"Content-Type": "application/json"})
    if int(user.status_code) == 400:
        user = httpx.post(url="http://localhost:9009/api/v1/auth/user",data=json.dumps(user_data,ensure_ascii=False))
        message_text = "Приветствуем Вас в нашем боте! Ваш аккаунт был успешно создан. Теперь вы можете использовать все возможности нашего бота."
    await message.answer(message_text,reply_markup=keyboard)


@dp.message(F.text == "Профиль")
async def view_profile(message: types.Message):
    kb = [[types.KeyboardButton(text="Изменить данные"),types.KeyboardButton(text="Удалить аккаунт")],[types.KeyboardButton(text="Главная страница")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
    await message.answer("Тут профиль!",reply_markup=keyboard)


    @dp.message(F.text == "Удалить аккаунт")
    async def delete_account(message: types.Message):
        kb = [[types.KeyboardButton(text="Да"),types.KeyboardButton(text="Нет")],[types.KeyboardButton(text="Главная страница")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
        await message.answer("Вы уверены, что хотите удалить аккаунт? Это действие необратимо!",reply_markup=keyboard)

        @dp.message(F.text == "Да")
        async def delete_account_yes(message: types.Message):
            httpx.delete(url="http://localhost:9009/api/v1/auth/user",params={"tg_id":message.from_user.id})
            await message.answer("Аккаунт удален!")

        @dp.message(F.text == "Нет")
        async def delete_account_no(message: types.Message):
            kb = [
                [types.KeyboardButton(text="Персонажи"),types.KeyboardButton(text="Профиль")],
                [types.KeyboardButton(text="Помощь"),types.KeyboardButton(text="Назначить сессию")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Что же вы выберете?")
            await message.answer("Аккаунт не удален!",keyboard=keyboard)


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
                put_data = {
                    "age": int(message.text),
                    "tg_id": message.from_user.id
                }    
                httpx.put(url="http://localhost:9009/api/v1/auth/user",json=put_data)
                kb = [[types.KeyboardButton(text="Главная страница")]]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Менялка")
                await message.answer("Вы успешно изменили возраст!",reply_markup=keyboard)

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
            kb = [[types.KeyboardButton(text="S"),types.KeyboardButton(text="A")],
                  [types.KeyboardButton(text="B"),types.KeyboardButton(text="C")],
                  [types.KeyboardButton(text="D"),types.KeyboardButton(text="E")],
                  [types.KeyboardButton(text="Главная страница")]]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
            await message.answer("Выберете вкладку по важности, остальное мы заполним сами :)",reply_markup=keyboard)
            @dp.message(F.text == "S")
            async def create_char_self_s(message: types.Message):
                kb = [[types.KeyboardButton(text="Имя")],[types.KeyboardButton(text="Раса")],
                      [types.KeyboardButton(text="Класс")],[types.KeyboardButton(text="Характеристики и модификаторы")], 
                      [types.KeyboardButton(text="Главная страница")]]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Выберете то, что хотите применить в создании персонажа")
                await message.answer("Здесь вы выбираете прям самое-самое основное",reply_markup=keyboard)
                char_data = {"Name":None,"Race":None,"Class":None,"Stats":None}


                @dp.message(F.text == "Имя")
                async def create_char_self_s_name(message: types.Message):
                    await message.answer("Введите имя персонажа")
                    @dp.message(F.text != "Имя")
                    async def create_char_self_s_name_not_name(message: types.Message):
                        char_data["Name"] = message.text
                
                @dp.message(F.text == "Класс")
                async def create_char_self_s_name(message: types.Message):
                    kb =  [[types.KeyboardButton(text="Воин"),types.KeyboardButton(text="Маг")],
                           [types.KeyboardButton(text="Вор"),types.KeyboardButton(text="Бард")],
                           [types.KeyboardButton(text="Следопыт"),types.KeyboardButton(text="Варвар")],
                           [types.KeyboardButton(text="Плут"),types.KeyboardButton(text="Друид")],
                           [types.KeyboardButton(text="Колдун"),types.KeyboardButton(text="Монах")],
                           [types.KeyboardButton(text="Паладин"),types.KeyboardButton(text="Жрец")],
                           [types.KeyboardButton(text="Волшебник")]]
                           
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Выберете класс")
                    await message.answer("Выберете класс",reply_markup=keyboard)
                    char_data["Class"] = message.text

                @dp.message(F.text == "Раса")
                async def create_char_self_s_race(message: types.Message):
                    kb = [[types.KeyboardButton(text="Дварф"),types.KeyboardButton(text="Эльф")],
                          [types.KeyboardButton(text="Полурослик"),types.KeyboardButton(text="Человек")],
                          [types.KeyboardButton(text="Драконорожденный"),types.KeyboardButton(text="Гном")],
                          [types.KeyboardButton(text="Полуэльф"),types.KeyboardButton(text="Полуорк")],
                          [types.KeyboardButton(text="Тифлинг")]]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Выберете расу")
                    await message.answer("Выберете расу",reply_markup=keyboard)
                    char_data["Race"] = message.text

                @dp.message(F.text == "Характеристики и модификаторы")
                async def create_char_self_s_stats(message: types.Message):
                    kb_num = [[types.KeyboardButton(text="15"),types.KeyboardButton(text="14"),
                               types.KeyboardButton(text="13"),types.KeyboardButton(text="12"),
                               types.KeyboardButton(text="10"),types.KeyboardButton(text="8")]]

                    kb = [[types.KeyboardButton(text="Сила"),types.KeyboardButton(text="Ловкость")],
                          [types.KeyboardButton(text="Телосложение"),types.KeyboardButton(text="Интеллект")],
                          [types.KeyboardButton(text="Мудрость"),types.KeyboardButton(text="Харизма")]]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Выберете характеристику")
                    await message.answer("Выберете характеристику",reply_markup=keyboard)
                    
                    #пока без логики
        @dp.message(F.text == "Пройти тест")
        async def test(message: types.Message):
            user_data = {"gender":None,"rac":None,"clas":None}
            kb = [[types.KeyboardButton(text="Пол"),types.KeyboardButton(text="Класс"),types.KeyboardButton(text="Раса")],
                [types.KeyboardButton(text="Главная страница")]]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Ууууу, да у кого-то тут персонажи!")
            await message.answer("Чтобы мы сделали персонажа за вас, выберете три характеристеки: пол, раса, класс",reply_markup=keyboard)
            
            
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