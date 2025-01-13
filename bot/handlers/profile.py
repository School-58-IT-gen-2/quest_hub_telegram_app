import asyncio

from aiogram import Dispatcher, types, Router
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.profile_keyboards import *
from keyboards.common_keyboards import *
from server_requests.profile_requests import *
from handlers.commands import main_menu
from forms import Form


dp = Dispatcher()
router = Router()

@router.callback_query(lambda c: c.data == 'profile') 
async def profile(callback_query: types.CallbackQuery):
    """Открытие меню профиля"""
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/profile.png")), reply_markup=account_menu_keyboard)

@router.callback_query(lambda c: c.data == 'change_profile')
async def change_profile(callback_query: types.CallbackQuery):
    """Открытие меню изменения провиля"""
    await callback_query.answer()
    await callback_query.message.edit_caption(reply_markup=change_user_data_keyboard)

@router.callback_query(lambda c: c.data == 'change_age')
async def change_age(callback_query: types.CallbackQuery, state: FSMContext):
    """Отправка сообщения при изменении возраста пользователя"""
    await callback_query.answer()
    await callback_query.message.edit_caption(caption="Введите ваш возраст")
    await state.set_state(Form.get_user_age)

@router.message(Form.get_user_age)
async def set_user_age(message: types.Message, state: FSMContext):
    """Установка нового возраста пользователя"""
    if message.text.isdigit():
        age = int(message.text)
        if age > 122:
            await message.answer(text="Жанна Кальман была самым старым задокументированным человеком в истории (122 года и 164 дня). Вряд ли нашим ботом пользуется кто-то старше неё. Пожалуйста попробуйте ещё раз.")
        else:
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
    else:
        await message.answer(text=f"Мне кажется {message.text} – это не ваш настоящий возраст... Пожалуйста попробуйте ещё раз.")

@router.callback_query(lambda c: c.data == 'delete_profile')
async def delete_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """Меню удаления пользователя"""
    await callback_query.answer()
    await callback_query.message.edit_caption(caption="Вы действительно хотите удалить профиль?", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.delete_profile_confirm)

@router.callback_query(Form.delete_profile_confirm)
async def confirm_delete_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """Меню подтверждения удаления пользователя"""
    await callback_query.answer()
    await state.clear()
    if callback_query.data == 'yes':
        await delete_user(tg_id = callback_query.from_user.id)
        await callback_query.message.edit_caption(caption="Ваш аккаунт был успешно удален")
        await asyncio.sleep(1.0)
        await callback_query.message.answer(text="Ваши данные успешно удалены. Для того чтобы продолжить пользоваться ботом нажмите /start")
    elif callback_query.data == 'no':
        await asyncio.sleep(1.0)
        await callback_query.message.delete()
        await main_menu(callback_query.message,text="Вы отменили удаление аккаунта")