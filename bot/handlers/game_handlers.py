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
from keyboards.character_keyboards import classes_keyboard
from server_requests.game_requests import *
from server_requests.character_requests.character_requests import get_char_by_user_id, get_char
from server_requests.profile_requests import get_user
from handlers.commands_handlers import main_menu_query, main_menu
from converter import game_card, game_character_card, tg_text_convert
from forms import Form


bot = Bot(token=os.getenv("BOT_TOKEN"))
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
        user_chars = await get_char_by_user_id(callback_query.from_user.id)
        if len(user_chars) == 0:
            await callback_query.message.edit_caption(caption="У вас ещё нет персонажей. Для присоединения к партиям необходимо наличие хотя бы одного персонажа.", reply_markup=create_new_characrer_keyboard)
            await state.set_state(Form.create_char_game_menu)
        else:
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

@router.callback_query(Form.create_char_game_menu)
async def create_char_game_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data == "back":
        await state.set_state(Form.choose_game_action)
        await callback_query.message.edit_caption(reply_markup=game_menu_keyboard)
    else:
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/char_create.png")))
        await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\n\nВыберите класс вашего персонажа:",  reply_markup=classes_keyboard)
        await state.set_state(Form.auto_char_class)
    
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
    if callback_query.data == "find_game":
        games = await get_game_filters(game_params)
        if len(games) > 0:
            game_arr = [[f'{game["name"]}', game["seed"]] for game in games]
            await callback_query.message.edit_text(text=f'Найдены партии ({len(games)}):', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(game_arr))))
            await state.set_state(Form.choose_game_menu)
        else:
            await callback_query.message.edit_text(text='*_Поиск партий:_*\n\nПартий с такими параметрами не существует\.',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))
    if callback_query.data == "back":
        await state.set_state(Form.choose_game_action)
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/session.png")), reply_markup=game_menu_keyboard)

@router.callback_query(Form.game_format_menu)
async def game_format_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Меню с форматом проведения партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game_params["format"] = callback_query.data if callback_query.data != "clear_filter" else None
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
    game_params["type"] = callback_query.data if callback_query.data != "clear_filter" else None
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
    game_params["level"] = callback_query.data if callback_query.data != "clear_filter" else None
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
        await state.clear()
        game_params["char_id"] = []
        game_params["master_id"] = str(callback_query.from_user.id)
        game = await create_game(game_params)
        await callback_query.message.edit_text(text=f"Вы создали новую партию \(сид: `{game["seed"]}`\):\n\n" + (await game_card(game_params)),parse_mode="MarkdownV2", reply_markup=await copy_seed_keyboard(game["seed"]))
        await callback_query.message.answer(text="Чтобы начать подбор игроков, вам необходимо:\n\n1. Создать группу и добавить туда этого бота.\n2. Сделать бота администратором.\n3. Начать диалог с ботом, используя команду /start.", reply_markup=tutorial_keyboard)

@router.message(Form.game_seed_menu)
async def game_seed_menu(message: types.Message, state: FSMContext):
    "Меню с сидом партии"
    game = await get_game_filters({"seed": message.text})
    if len(game) == 0:
        await message.answer(text='Партии с таким сидом не существует. Пожалуйста, введите действительный сид:', reply_markup=back_keyboard)
    else:
        game = game[0]
        await state.update_data({"game": game})
        reply_markup = join_game_keyboard if game["type"] == "Открытая" else request_join_game_keyboard
        if message.from_user.id == int(game["master_id"]):
            reply_markup = back_keyboard
        await message.answer(text=f"Найдена партия {game["name"]} \(сид: `{game["seed"]}`\):\n\n" + (await game_card(game)),parse_mode="MarkdownV2", reply_markup=reply_markup)
        await state.set_state(Form.join_game_menu)

@router.callback_query(Form.join_game_menu)
async def join_game_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Присоединение к найденной партии"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    games = await get_game_filters(game_params)
    if callback_query.data == "back":
        game_arr = [[f'{game["name"]}', game["seed"]] for game in games]
        await callback_query.message.edit_text(text=f'Найдены партии ({len(games)}):', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(game_arr))))
        await state.set_state(Form.choose_game_menu)
    else:
        user_chars = await get_char_by_user_id(callback_query.from_user.id)
        char_arr = [[f'{char["name"]} {char["surname"]}', str(char["id"])] for char in user_chars]
        await callback_query.message.edit_text(text='Выберите персонажа, которого вы хотите отыгрывать в партии:', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(char_arr))))
        await state.set_state(Form.choose_char_menu)

@router.callback_query(Form.choose_char_menu)
async def choose_char_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Выбор персонажа для партии"""
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    game = (await state.get_data())["game"]
    if 'left' in callback_query.data or 'right' in callback_query.data:
        user_chars = await get_char_by_user_id(callback_query.from_user.id)
        char_arr = [[f'{char["name"]} {char["surname"]}', str(char["id"])] for char in user_chars]
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=(await change_keyboard_page(callback_query.data, char_arr))))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))
        await state.set_state(Form.game_filters_menu)
    else:
        char = (await get_char(callback_query.data))[0]
        reply_markup = back_keyboard if callback_query.from_user.id == int(game["master_id"]) else choose_game_character_keyboard
        await callback_query.message.edit_text(text=(await game_character_card(char)),parse_mode="MarkdownV2",reply_markup=reply_markup)
        await state.set_state(Form.game_send_char_menu)
        await state.update_data({"char": char})

@router.callback_query(Form.choose_game_menu)
async def choose_game_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Выбор партии"""
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    games = await get_game_filters(game_params)
    if 'left' in callback_query.data or 'right' in callback_query.data:
        game_arr = [[f'{game["name"]}', game["seed"]] for game in games]
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=(await change_keyboard_page(callback_query.data, game_arr))))
    elif callback_query.data == "dict_kb_back":
        await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))
        await state.set_state(Form.game_filters_menu)
    else:
        game = (await get_game_filters({"seed": callback_query.data}))[0]
        await state.update_data({"game": game})
        reply_markup = back_keyboard if callback_query.from_user.id == int(game["master_id"]) else choose_game_character_keyboard
        await callback_query.message.edit_text(text=(await game_card(game)),parse_mode="MarkdownV2",reply_markup=reply_markup)
        await state.set_state(Form.join_game_menu)

@router.callback_query(Form.game_send_char_menu)
async def game_send_char_menu(callback_query: types.CallbackQuery, state: FSMContext):
    "Отправка заявки на присоединение к партии"
    await callback_query.answer()
    data = (await state.get_data())
    game = data["game"]
    char = data["char"]
    if callback_query.data == "back":
        user_chars = await get_char_by_user_id(callback_query.from_user.id)
        char_arr = [[f'{char["name"]} {char["surname"]}', str(char["id"])] for char in user_chars]
        await callback_query.message.edit_text(text='Выберите персонажа, которого вы хотите отыгрывать в партии:', reply_markup=InlineKeyboardMarkup(inline_keyboard=(await build_arr_keyboard(char_arr))))
        await state.set_state(Form.choose_char_menu)
    elif game["type"] == "Открытая":
        link = (await bot.create_chat_invite_link(int(game["chat_id"]))).invite_link
        await bot.send_message(int(game["chat_id"]), text="К партии присоединился новый персонаж:\n\n" + (await game_character_card(char)),parse_mode="MarkdownV2")
        game["char_id"].append(char["user_id"])
        if len(game["char_id"]) == game["player_count"]:
            game["active"] = False
            await bot.send_message(int(game["chat_id"]), text="Набор игроков в партию завершился.")
        await update_game(game)
        await state.update_data({"game": game})
        await callback_query.message.edit_text(text="Вы можете присоединиться к партии по ссылке:", reply_markup=await url_join_game_keyboard(link))
    elif game["type"] == "Закрытая":
        await bot.send_message(chat_id=game["master_id"], text=f'К вашей партии {await tg_text_convert(game["name"])}  \(сид: `{game["seed"]}`\) хочет присоединиться новый персонаж:\n\n' + (await game_character_card(char)), parse_mode="MarkdownV2", reply_markup=await approve_char_keyboard(char["id"], game["seed"]))
        await callback_query.message.delete()
        await main_menu(callback_query.message, state, "Ваша карточка персонажа была отправлена владельцу партии. Ожидайте уведомления о его решении.")


@router.callback_query(Form.game_seed_menu)
async def clear_game_seed(callback_query: types.CallbackQuery, state: FSMContext):
    "Отмена поиска партии по сиду"
    await callback_query.answer()
    game_params = (await state.get_data())["game_params"]
    await state.set_state(Form.game_filters_menu)
    await callback_query.message.edit_text(text='*_Поиск партий:_*',parse_mode="MarkdownV2",reply_markup=(await game_filters_keyboard(game_params)))

@router.message(Form.connect_game_chat)
async def connect_game_chat(message: types.Message, state: FSMContext):
    "Привязка чата к партии"
    game = await get_game_seed(message.text)
    if not game:
        await message.answer(text='Партии с таким сидом не существует. Пожалуйста, введите действительный сид:')
    else:
        if int(game["master_id"]) == message.from_user.id:
            if len(game["char_id"]) == game["player_count"]:
                await message.answer("Набор игроков в эту партию уже завершён.")
            game["active"] = True
            game["chat_id"] = str(message.chat.id)
            await update_game(game)
            await state.update_data({"game_params": game})
            await message.answer(text=f"Найдена партия {game["name"]} \(сид: `{game["seed"]}`\):\n\nТеперь в данный чат будут отправляться персонажи присоединившихся игроков\.\n\n" + (await game_card(game)),parse_mode="MarkdownV2")
        else:
            await message.answer("Вы не являетесь владельцем этой партии.")

@router.callback_query(lambda c: "approve_" in c.data)
async def approve_char(callback_query: types.CallbackQuery, state: FSMContext):
    "Подтверждение присоединения персонажа к партии"
    await callback_query.answer()
    char = (await get_char(callback_query.data.split('_')[1]))[0]
    game = (await get_game_filters({"seed": callback_query.data.split('_')[2]}))[0]
    game["char_id"].append(char["user_id"])
    link = (await bot.create_chat_invite_link(int(game["chat_id"]))).invite_link
    await bot.send_message(int(char["user_id"]), text=f'Ваша заявка на присоединение к партии {await tg_text_convert(game["name"])} \(сид: `{game["seed"]}`\) была одобрена\.',parse_mode="MarkdownV2", reply_markup=await url_join_game_keyboard(link))
    await bot.send_message(int(game["chat_id"]), text="К партии присоединился новый персонаж:\n\n" + (await game_character_card(char)),parse_mode="MarkdownV2")
    await callback_query.message.edit_text("Персонаж был одобрен.")
    if len(game["char_id"]) == game["player_count"]:
        game["active"] = False
        await bot.send_message(int(game["chat_id"]), text="Набор игроков в партию завершился.")
    await update_game(game)
    await state.update_data({"game": game})

@router.callback_query(lambda c: "decline_" in c.data)
async def decline_char(callback_query: types.CallbackQuery, state: FSMContext):
    "Отклонение присоединения персонажа к партии"
    await callback_query.answer()
    char = (await get_char(callback_query.data.split('_')[1]))[0]
    game = (await get_game_filters({"seed": callback_query.data.split('_')[2]}))[0]
    await bot.send_message(int(char["user_id"]), text=f'Ваша заявка на присоединение к партии {await tg_text_convert(game["name"])} \(сид: `{game["seed"]}`\) была отклонена её владельцем\.', parse_mode="MarkdownV2")
    await callback_query.message.edit_text("Персонаж был отклонён.")