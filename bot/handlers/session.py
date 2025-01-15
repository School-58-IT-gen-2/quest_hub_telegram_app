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

from keyboards.session_keyboards import *
from keyboards.common_keyboards import *
from server_requests.session_requests import *
from handlers.commands import main_menu
from forms import Form
from converter import convert_json_to_char_info


dp = Dispatcher()
router = Router()

@router.callback_query(lambda c: c.data == 'arrange_meeting')
async def arrange_meeting(callback_query: types.CallbackQuery):
    """Открытие меню для сессий"""
    await callback_query.answer()
<<<<<<< HEAD
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/session.png")), reply_markup=session_menu_keyboard)   
=======
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/session.png")), reply_markup=session_menu_keyboard)    
>>>>>>> 603cedb1e1fe5f189c0626ecf3752f81ae7a2410
