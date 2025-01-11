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
from converter import convert_json_to_char_info


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
    await message.answer_photo(caption=message_text,photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard)

async def clear_chat(message: types.Message, bot: Bot):
    for i in range(message.message_id-25,message.message_id+1):
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=i)
        except:
            pass
        

@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Тут помощь (возможно)!")

async def main_menu(message: types.Message, text: str):
    await message.answer_photo(caption=text,photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard)

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
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup = await build_char_kb(user_chars))
    await state.set_state(Form.view_character)

@router.callback_query(Form.view_character)
async def view_char(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.clear()
    char = await get_char_by_char_id(int(callback_query.data))
    await callback_query.message.answer(text=f"```\n{json.dumps(char[0],indent=2, ensure_ascii=False)}\n```",parse_mode="Markdown",reply_markup=change_or_delete_character) 
    await state.update_data({"created_message_id": callback_query.message.message_id})
    await state.update_data({"char": char[0]})

@router.callback_query(lambda c: c.data == 'put_character')
async def put_character(callback_query: types.CallbackQuery,state: FSMContext, bot: Bot):
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    await update_char(char, char["id"])
    await clear_chat(callback_query.message, bot)
    await main_menu(callback_query.message,text="")
    await callback_query.message.edit_caption(caption="Ваш персонаж успешно обновлён!", reply_markup=main_menu_keyboard)
    
@router.callback_query(lambda c: c.data == 'delete_character')
async def delete_character(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы уверены в своих действиях?", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.delete_character_confirm)

@router.callback_query(Form.delete_character_confirm)
async def delete_character_confirm(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "yes":
        await callback_query.message.edit_text(text="Вы удалили персонажа")
        await asyncio.sleep(1)
        await delete_char(char["id"])
        await clear_chat(callback_query.message, bot)
        await main_menu(callback_query.message,text="Вы жестоко удалили вашего персонажа!")
    if callback_query.data == "no":
        await callback_query.message.edit_text(text="Вы отменили удаление персонажа")
        await asyncio.sleep(1)
        await clear_chat(callback_query.message, bot)
        await main_menu(callback_query.message,text="Вы помиловали вашего персонажа от удаления!")


@router.callback_query(lambda c: c.data == 'back')
async def get_back(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    await state.set_state(Form.view_character)

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
async def set_user_age(message: types.Message, state: FSMContext, bot: Bot):
    # Здесь должно записыаться в БД
    age = int(message.text)
    await message.answer_photo(photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard, caption=f"Ваш возраст изменен на {message.text}")
    user_data = {
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "role": "player",
            "is_bot": message.from_user.is_bot,
            "language_code": message.from_user.language_code,
            "is_premium": message.from_user.is_premium,
            "username": message.from_user.username,
            "age": age,
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
async def confirm_delete_profile(callback_query: types.CallbackQuery, state: FSMContext,bot : Bot):
    await callback_query.answer()
    await state.clear()
    if callback_query.data == 'yes':
        await delete_user(tg_id = callback_query.from_user.id)
        await callback_query.message.edit_caption(caption="Ваш аккаунт был успешно удален")
        await asyncio.sleep(1.0)
        await clear_chat(callback_query.message, bot)
        await callback_query.message.answer(text="Ваши данные успешно удалены. Для того чтобы продолжить пользоваться ботом нажмите /start")
    elif callback_query.data == 'no':
        await callback_query.message.edit_caption(caption="Вы отменили удаление аккаунта")
        await asyncio.sleep(1.0)
        await callback_query.message.delete()
        await main_menu(callback_query.message,text="")
    

@router.callback_query(lambda c: c.data == 'create_character')
async def choose_creation(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/char_create.png")))
    await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\nВыберете класс вашего персонажа:",  reply_markup=classes_keyboard)
    await state.set_state(Form.auto_char_class)

@router.callback_query(Form.auto_char_class)
async def enter_char_class(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data({"character_class": callback_query.data})
    await callback_query.message.edit_caption(caption="Выберете расу вашего персонажа:",reply_markup=races_keyboard)
    await state.set_state(Form.auto_char_race)

@router.callback_query(Form.auto_char_race)
async def enter_char_race(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data({"race": callback_query.data})
    await callback_query.message.edit_caption(caption="Выберете пол вашего персонажа:",reply_markup=gender_keyboard)
    await state.set_state(Form.auto_char_gender)

@router.callback_query(Form.auto_char_gender)
async def enter_char_gender(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data({"gender": callback_query.data})
    response = await auto_create_char(await state.get_data())
    response["user_id"] = callback_query.from_user.id
    await callback_query.message.delete()
    await callback_query.message.answer(text=convert_json_to_char_info(response),parse_mode="MarkdownV2",reply_markup=what_do_next)
    await state.clear()
    await state.update_data({"created_message_id": callback_query.message.message_id})
    await state.update_data({"char" : response})
    
@router.callback_query(lambda c: c.data == 'discard_character')
async def discard_character(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы действительно хотите удалить персонажа?", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.discard_character)
    
@router.callback_query(Form.discard_character)
async def discard_character(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback_query.answer()
    if callback_query.data == 'yes':
        created_message_id = await state.get_data()
        created_message_id = created_message_id["created_message_id"]
        now_message_id = callback_query.message.message_id
        if now_message_id - 1 == created_message_id:
            await callback_query.message.delete()
            await main_menu(callback_query.message, text="")
            await state.clear()
        else:
            await clear_chat(callback_query.message, bot)
            await callback_query.message.answer_photo(photo=FSInputFile("assets/main_menu.png"),reply_markup=main_menu_keyboard)
            await state.update_data({"created_message_id": callback_query.message.message_id})
    else:
        await callback_query.message.edit_text(text="Вы отменили удаление персонажа",reply_markup=what_do_next)

@router.callback_query(lambda c: c.data == 'save_character')
async def save_character(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    response = await create_char(char)
    await callback_query.message.answer(text=f"```\n{json.dumps(response,indent=2, ensure_ascii=False)}\n```",parse_mode="Markdown")

@router.callback_query(lambda c: c.data == 'update_character')
async def update_character(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()
    text = await state.get_data()
    text = json.dumps(text["char"],indent=2, ensure_ascii=False)
    await state.update_data({"char": json.loads(text)})
    await callback_query.message.edit_reply_markup(reply_markup=change_character)

@router.callback_query(lambda c: c.data == 'char_name')
async def enter_char_name(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(text="Введите имя персонажа:")
    await state.set_state(Form.char_name)

@router.message(Form.char_name)
async def char_name(message: types.Message,state: FSMContext):
    name = message.text
    char = await state.get_data()
    char = char["char"]
    char["name"] = name
    created_message_id = await state.get_data()
    created_message_id = created_message_id["created_message_id"]
    await message.answer(text=f"Ваш персонаж после правок:\n```\n{json.dumps(char,indent=2, ensure_ascii=False)}\n```",parse_mode="Markdown",reply_markup=what_do_next)
    await state.clear()
    await state.update_data({"created_message_id": created_message_id})
    await state.update_data({"char" : char})


@router.callback_query(lambda c: c.data == 'char_age')
async def enter_char_age(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(text="Введите возраст персонажа:")
    await state.set_state(Form.char_age)

@router.message(Form.char_age)
async def char_age(message: types.Message,state: FSMContext):
    age = int(message.text)
    print(age)
    char = await state.get_data()
    char = char["char"]
    char["age"] = age
    created_message_id = await state.get_data()
    created_message_id = created_message_id["created_message_id"]
    await message.answer(text=f"Ваш персонаж после правок:\n```\n{json.dumps(char,indent=2, ensure_ascii=False)}\n```",parse_mode="Markdown",reply_markup=what_do_next)   
    await state.clear()
    await state.update_data({"created_message_id": created_message_id})
    await state.update_data({"char" : char})
    
@router.callback_query(lambda c: c.data == 'char_surname')
async def enter_char_surname(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(text="Введите фамилию персонажа:")
    await state.set_state(Form.char_name)

@router.message(Form.char_surname)
async def char_surname(message: types.Message,state: FSMContext):
    surname = message.text
    char = await state.get_data()
    char = char["char"]
    char["surname"] = surname
    created_message_id = await state.get_data()
    created_message_id = created_message_id["created_message_id"]
    await message.answer(text=f"Ваш персонаж после правок:\n```\n{json.dumps(char,indent=2, ensure_ascii=False)}\n```",parse_mode="Markdown",reply_markup=what_do_next)
    await state.clear()
    await state.update_data({"created_message_id": created_message_id})
    await state.update_data({"char" : char})


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())