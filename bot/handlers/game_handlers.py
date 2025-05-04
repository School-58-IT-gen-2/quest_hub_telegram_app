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

from keyboards.game_keyboards import *
from keyboards.common_keyboards import *
from server_requests.game_requests import *
from handlers.commands_handlers import main_menu_query
from converter import game_card
from forms import Form


dp = Dispatcher()
router = Router()

@router.callback_query(lambda c: c.data == 'arrange_meeting')
async def games_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню для партий"""
    await callback_query.answer()
    await state.set_state(Form.choose_game_action)
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/session.png")), reply_markup=game_menu_keyboard)

@router.callback_query(Form.choose_game_action)
async def choose_game_action(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с партиями"
    await callback_query.answer()
    if callback_query.data == "create_game":
        await callback_query.answer()
        await state.update_data({"game_action": "create_game"})
        await state.update_data({"game_params": {
                "type": None,
                "format": None,
                "city": None,
                "level": None,
                "player_count": None,
                "name": None,
                "description": None
            }})
        await callback_query.message.delete()
        await callback_query.message.answer(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard()))
        await state.set_state(Form.game_params_menu)
    if callback_query.data == "find_game":
        await callback_query.answer()
        await state.update_data({"game_action": "find_game"})
        await state.update_data({"game_params": {
                "type": None,
                "format": None,
                "city": None,
                "level": None,
                "player_count": None,
                "name": None,
                "seed": None
            }})
        await callback_query.message.delete()
        await callback_query.message.answer(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard()))
        await state.set_state(Form.game_filters_menu)
    if callback_query.data == "main_menu":
        await main_menu_query(callback_query, state)
    
@router.callback_query(Form.game_params_menu)
async def game_params_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с параметрами партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    if callback_query.data == "format":
        await callback_query.message.edit_text(text='Выберите формат проведения партии:',reply_markup=game_format_keyboard)
        await state.set_state(Form.game_format_menu)
    if callback_query.data == "type":
        await callback_query.message.edit_text(text='Выберите тип партии:',reply_markup=game_type_keyboard)
        await state.set_state(Form.game_type_menu)
    if callback_query.data == "level":
        await callback_query.message.edit_text(text=(
            'Выберите уровень, на который расчитана ваша партия:\n\n'
            'Лёгкий – требуется уровень персонажа 1-5.\n'
            'Средний – требуется уровень персонажа 5-10.\n'
            'Сложный – требуется уровень персонажа 10-15.\n'
            'Социальный – важно уменее отыгрывать персонажа, а не боевые характеристики.'
        ),reply_markup=game_level_keyboard)
        await state.set_state(Form.game_level_menu)
    if callback_query.data == "name":
        await callback_query.message.edit_text(text='Напишите название для вашей партии:')
        await state.set_state(Form.game_name_menu)
    if callback_query.data == "description":
        await callback_query.message.edit_text(text='Напишите описание для вашей партии:')
        await state.set_state(Form.game_description_menu)
    if callback_query.data == "player_count":
        await callback_query.message.edit_text(text='Введите количество игроков, на которое расчитана ваша партия:')
        await state.set_state(Form.game_player_count_menu)
    if callback_query.data == "city":
        await state.update_data({"game_params": game_params})
        if game_params["format"] == "Оффлайн":
            await callback_query.message.edit_text(text='Введите название города, в котором проводится партия:')
        else:
            await callback_query.message.edit_text(text='Формат партии изменён на «Оффлайн». Введите название города, в котором проводится партия:')
        game_params["format"] = "Оффлайн"
        await state.set_state(Form.game_city_menu)
    if callback_query.data == "game_ready":
        if not game_params["type"]:
            await callback_query.message.edit_text(text='Для создания партии необходимо указать её тип.',reply_markup=(await game_params_keyboard(game_params)))
        elif not game_params["format"]:
            await callback_query.message.edit_text(text='Для создания партии необходимо указать её формат.',reply_markup=(await game_params_keyboard(game_params)))
        elif game_params["format"] == "Оффлайн" and (not game_params["city"]):
            await callback_query.message.edit_text(text='Если партия проводится оффлайн, то необходимо указать город её проведения.',reply_markup=(await game_params_keyboard(game_params)))
        elif not game_params["player_count"]:
            await callback_query.message.edit_text(text='Для создания партии необходимо указать количество игроков.',reply_markup=(await game_params_keyboard(game_params)))
        elif not game_params["name"]:
            await callback_query.message.edit_text(text='Для создания партии необходимо указать её название.',reply_markup=(await game_params_keyboard(game_params)))
        else:
            await callback_query.message.edit_text(text=(await game_card(game_params)),reply_markup=create_game_keyboard,parse_mode="MarkdownV2")
            await state.set_state(Form.game_ready)
    if callback_query.data == "back":
        await state.set_state(Form.choose_game_action)
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/session.png")), reply_markup=game_menu_keyboard)

@router.callback_query(Form.game_filters_menu)
async def game_filters_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с фильтрами поиска"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    if callback_query.data == "format":
        await callback_query.message.edit_text(text='Выберите формат проведения партии:',reply_markup=game_format_filter_keyboard)
        await state.set_state(Form.game_format_menu)
    if callback_query.data == "type":
        await callback_query.message.edit_text(text='Выберите тип партии:',reply_markup=game_type_filter_keyboard)
        await state.set_state(Form.game_type_menu)
    if callback_query.data == "level":
        await callback_query.message.edit_text(text=(
            'Выберите уровень партии, которую вы ищите:\n\n'
            'Лёгкий – требуется уровень персонажа 1-5.\n'
            'Средний – требуется уровень персонажа 5-10.\n'
            'Сложный – требуется уровень персонажа 10-15.\n'
            'Социальный – важно уменее отыгрывать персонажа, а не боевые характеристики.'
        ),reply_markup=game_level_filter_keyboard)
        await state.set_state(Form.game_level_menu)
    if callback_query.data == "name":
        await callback_query.message.edit_text(text='Напишите название партии, которую вы ищите:', reply_markup=clear_filter_keyboard)
        await state.set_state(Form.game_name_menu)
    if callback_query.data == "player_count":
        await callback_query.message.edit_text(text='Введите желаемое количество игроков в партии:', reply_markup=clear_filter_keyboard)
        await state.set_state(Form.game_player_count_menu)
    if callback_query.data == "city":
        await state.update_data({"game_params": game_params})
        if game_params["format"] == "Оффлайн":
            await callback_query.message.edit_text(text='Введите название города, в котором проводится партия:', reply_markup=clear_filter_keyboard)
        else:
            await callback_query.message.edit_text(text='Формат партии изменён на «Оффлайн». Введите название города, в котором проводится партия:', reply_markup=clear_filter_keyboard)
        game_params["format"] = "Оффлайн"
        await state.set_state(Form.game_city_menu)
    if callback_query.data == "clear_filters":
        await state.update_data({"game_params": {
                "type": None,
                "format": None,
                "city": None,
                "level": None,
                "player_count": None,
                "name": None,
                "seed": None
            }})
        await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard()))
    if callback_query.data == "find_game_seed":
        await callback_query.message.edit_text(text='Введите сид партии, которую вы ищите:', reply_markup=back_keyboard)
        await state.set_state(Form.game_seed_menu)
    if callback_query.data == "back":
        await state.set_state(Form.choose_game_action)
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/session.png")), reply_markup=game_menu_keyboard)

@router.callback_query(Form.game_format_menu)
async def game_format_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с форматом проведения партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game_params["format"] = callback_query.data
    if callback_query.data == "Онлайн":
        game_params["city"] = None
    await state.update_data({"game_params": game_params})
    if "description" in game_params:
        await state.set_state(Form.game_params_menu)
        await callback_query.message.edit_text(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
    else:
        await state.set_state(Form.game_filters_menu)
        await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.callback_query(Form.game_type_menu)
async def game_type_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с типом партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game_params["type"] = callback_query.data
    await state.update_data({"game_params": game_params})
    if "description" in game_params:
        await state.set_state(Form.game_params_menu)
        await callback_query.message.edit_text(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
    else:
        await state.set_state(Form.game_filters_menu)
        await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.callback_query(Form.game_level_menu)
async def game_level_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с уровнем партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game_params["level"] = callback_query.data
    await state.update_data({"game_params": game_params})
    if "description" in game_params:
        await state.set_state(Form.game_params_menu)
        await callback_query.message.edit_text(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
    else:
        await state.set_state(Form.game_filters_menu)
        await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.message(Form.game_name_menu)
async def game_name_menu(message: types.Message, state: FSMContext):
    "Меню с названием партии"
    game_params = (await state.get_data())["game_params"]
    game_params["name"] = message.text
    await state.update_data({"game_params": game_params})
    if "description" in game_params:
        await state.set_state(Form.game_params_menu)
        await message.answer(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
    else:
        await state.set_state(Form.game_filters_menu)
        await message.answer(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.callback_query(Form.game_name_menu)
async def clear_game_name(callback_query: types.CallbackQuery, state: FSMContext):
    "Очистка фильтра названия партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game_params["name"] = None
    await state.update_data({"game_params": game_params})
    await state.set_state(Form.game_filters_menu)
    await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.message(Form.game_description_menu)
async def game_description_menu(message: types.Message, state: FSMContext):
    "Меню с описанием партии"
    game_params = (await state.get_data())["game_params"]
    game_params["description"] = message.text
    await state.update_data({"game_params": game_params})
    await state.set_state(Form.game_params_menu)
    await message.answer(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))

@router.message(Form.game_city_menu)
async def game_city_menu(message: types.Message, state: FSMContext):
    "Меню с городом партии"
    game_params = (await state.get_data())["game_params"]
    game_params["city"] = message.text
    await state.update_data({"game_params": game_params})
    if "description" in game_params:
        await state.set_state(Form.game_params_menu)
        await message.answer(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
    else:
        await state.set_state(Form.game_filters_menu)
        await message.answer(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.callback_query(Form.game_city_menu)
async def clear_game_city(callback_query: types.CallbackQuery, state: FSMContext):
    "Очистка фильтра города партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game_params["city"] = None
    await state.update_data({"game_params": game_params})
    await state.set_state(Form.game_filters_menu)
    await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.message(Form.game_player_count_menu)
async def game_player_count_menu(message: types.Message, state: FSMContext):
    "Меню с количеством игроков в партии партии"
    game_params = (await state.get_data())["game_params"]
    if message.text.isdigit():
        if int(message.text) > 100:
            await message.answer(text="Как-то многовато людей для одной партии. Пожалуйста, введите действительное число игроков.")
        elif int(message.text) == 0:
            await message.answer("Очень грустно, если в партии 0 игроков. Пожалуйста, введите действительное число игроков.")
        else:
            game_params["player_count"] = int(message.text)
            await state.update_data({"game_params": game_params})
            if "description" in game_params:
                await state.set_state(Form.game_params_menu)
                await message.answer(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
            else:
                await state.set_state(Form.game_filters_menu)
                await message.answer(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))
    else:
        await message.answer(text=f"Вы хотите сказать, что в партии {message.text} игроков? Пожалуйста, введите действительное число игроков.")

@router.callback_query(Form.game_player_count_menu)
async def clear_game_player_count(callback_query: types.CallbackQuery, state: FSMContext):
    "Очистка фильтра количества игроков в партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game_params["player_count"] = None
    await state.update_data({"game_params": game_params})
    await state.set_state(Form.game_filters_menu)
    await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.callback_query(Form.game_ready)
async def game_ready(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с подтверждением создания партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    if callback_query.data == "back":
        await state.set_state(Form.game_params_menu)
        await callback_query.message.edit_text(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
    else:
        game = {
            "name": game_params["name"],
            "description": game_params["description"],
            "is_online": True if game_params["format"] == "Онлайн" else False,
            "place": game_params["city"],
            "game_level": game_params["level"],
            "number_of_players": int(game_params["player_count"]),
            "master_id": str(callback_query.from_user.id),
            "players_id": [],
            "seed": "test"
        }
        game = await create_game(game)
        await callback_query.message.edit_text(text=f"Вы создали новую партию \(сид: `{game["seed"]}`\):\n\n" + (await game_card(game_params)),parse_mode="MarkdownV2")

@router.message(Form.game_seed_menu)
async def game_seed_menu(message: types.Message, state: FSMContext):
    "Меню с сидом партии"
    game = await get_game_filters({"seed": message.text})
    if len(game) == 0:
        await message.answer(text='Партии с таким сидом не существует. Пожалуйста, введите действительный сид:', reply_markup=back_keyboard)
    else:
        game_params = {
            "type": "Открытая" | "Закрытая",
            "format": "Онлайн" | "Оффлайн",
            "city": "",
            "level": "Лёгкий" | "Средний" | "Сложный" | "Социальный",
            "player_count": None,
            "name": None
        }
        await message.answer(text=f"Вы создали новую партию \(сид: `{game["seed"]}`\):\n\n" + (await game_card(game_params)),parse_mode="MarkdownV2")
    game_params = (await state.get_data())["game_params"]
    game_params["city"] = message.text
    await state.update_data({"game_params": game_params})
    if "description" in game_params:
        await state.set_state(Form.game_params_menu)
        await message.answer(text='*_Создание партии:_*',parse_mode="MarkdownV2",reply_markup=(await game_params_keyboard(game_params)))
    else:
        await state.set_state(Form.game_filters_menu)
        await message.answer(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.callback_query(Form.game_seed_menu)
async def clear_game_seed(callback_query: types.CallbackQuery, state: FSMContext):
    "Отмена поиска партии по сиду"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    await state.set_state(Form.game_filters_menu)
    await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))