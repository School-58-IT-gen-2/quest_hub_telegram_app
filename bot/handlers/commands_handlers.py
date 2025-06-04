from aiogram import Dispatcher, types, Router, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import *
from server_requests.profile_requests import *
from converter import *
from forms import Form


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
router = Router()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    """Вывод приветствия и создание пользователя"""
    await state.clear()
    if message.chat.type == 'private':
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
    elif message.chat.type == 'group':
        if (await message.chat.get_member(TOKEN.split(":")[0])).status != "administrator":
            await message.answer(text="Пожалуйста, сделайте бота администратором и попробуйте ещё раз.")
        else:
            if (await message.chat.get_member(message.from_user.id)).status != "creator":
                await message.answer("Только владелец группы может взаимодействовать с ботом.")
            else:
                await message.answer(text="Введите сид вашей партии:")
                await state.set_state(Form.connect_game_chat)

@router.callback_query(lambda c: c.data == 'main_menu')
async def main_menu_query(callback_query: types.CallbackQuery, state: FSMContext):
    """Вывод главного меню (редактирование сообщения)"""
    await callback_query.answer()
    await state.clear()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/main_menu.png")), reply_markup=main_menu_keyboard)

async def main_menu(message: types.Message, state: FSMContext, text: str = ""):
    """Вывод главного меню (отправка нового сообщения)"""
    await state.clear()
    await message.answer_photo(caption=text,photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard)
