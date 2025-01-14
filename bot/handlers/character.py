import asyncio
import json

from aiogram import Dispatcher, types, Router
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests import *
from handlers.commands import main_menu, main_menu_query
from forms import Form
from converter import convert_json_to_char_info


dp = Dispatcher()
router = Router()

@router.callback_query(lambda c: c.data == 'characters')
async def characters(callback_query: types.CallbackQuery):
    """Открытие меню персонажей"""
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)

@router.callback_query(lambda c: c.data == 'view_characters')
async def view_characters(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие списка всех персонажей пользователя"""
    await callback_query.answer()
    user_chars = await get_char_by_user_id(callback_query.from_user.id)
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup = await build_char_kb(user_chars))
    await state.set_state(Form.view_character)

@router.callback_query(Form.view_character)
async def view_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Вывод персонажа"""
    await callback_query.answer()
    await state.clear()
    if callback_query.data == 'main_menu':
        await main_menu_query(callback_query)
    else:
        char = await get_char_by_char_id(int(callback_query.data))
        char = char[0]
        await callback_query.message.answer(text=convert_json_to_char_info(char),parse_mode="MarkdownV2",reply_markup=change_or_delete_character) 
        await state.update_data({"char": char})

@router.callback_query(lambda c: c.data == 'put_character')
async def put_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Обновление данных персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=put_change_character)
    
@router.callback_query(lambda c: c.data == 'put_char_name')
async def put_char_name(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(text="Введите новое имя персонажа")
    await state.set_state(Form.put_char_name)

@router.message(Form.put_char_name)
async def put_char_name_confirm(message: types.Message, state: FSMContext):
    name = message.text
    char = await state.get_data()
    char = char["char"]
    char["name"] = name
    await update_char(char,char["id"])
    await message.answer(text=convert_json_to_char_info(char),parse_mode="MarkdownV2",reply_markup=change_or_delete_character)
    await state.clear()
    await state.update_data({"char": char})

@router.callback_query(lambda c: c.data == 'put_char_age')
async def put_char_age(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(text="Введите новый возраст персонажа")
    await state.set_state(Form.put_char_age)

@router.message(Form.put_char_age)
async def put_char_age_confirm(message: types.Message, state: FSMContext):
    age = message.text
    char = await state.get_data()
    char = char["char"]
    char["age"] = age
    await update_char(char,char["id"])
    await message.answer(text=convert_json_to_char_info(char),parse_mode="MarkdownV2",reply_markup=change_or_delete_character)
    await state.clear()
    await state.update_data({"char": char})

@router.callback_query(lambda c: c.data == 'put_char_surname')
async def put_char_surname(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(text="Введите новую фамилию персонажа")
    await state.set_state(Form.put_char_surname)

@router.message(Form.put_char_surname)
async def put_char_surname_confirm(message: types.Message, state: FSMContext):
    surname = message.text
    char = await state.get_data()
    char = char["char"]
    char["surname"] = surname
    await update_char(char,char["id"])
    await message.answer(text=convert_json_to_char_info(char),parse_mode="MarkdownV2",reply_markup=change_or_delete_character)
    await state.clear()
    await state.update_data({"char": char})

@router.callback_query(lambda c: c.data == 'delete_character')
async def delete_character(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню удаления персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы уверены в своих действиях?", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.delete_character_confirm)

@router.callback_query(Form.delete_character_confirm)
async def delete_character_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню подтверждения удаления персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "yes":
        await delete_char(char["id"])
        await main_menu(callback_query.message,text="Вы жестоко удалили вашего персонажа!")
    if callback_query.data == "no":
        await callback_query.message.edit_text(parse_mode="MarkdownV2",text=f"{convert_json_to_char_info(char)}\nВы отказались от удаления персонажа",reply_markup=change_or_delete_character)

@router.callback_query(lambda c: c.data == 'back')
async def get_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Возврат к просмотру персонажа"""
    await callback_query.answer()
    await callback_query.message.delete()
    await state.set_state(Form.view_character)

@router.callback_query(lambda c: c.data == 'create_character')
async def choose_creation(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие меню с выбором класса персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/char_create.png")))
    await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\nВыберете класс вашего персонажа:",  reply_markup=classes_keyboard)
    await state.set_state(Form.auto_char_class)

@router.callback_query(Form.auto_char_class)
async def enter_char_class(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню с выбором расы персонажа"""
    await callback_query.answer()
    if callback_query.data == 'main_menu':
        await main_menu_query(callback_query)
    else:
        await state.update_data({"character_class": callback_query.data})
        await callback_query.message.edit_caption(caption="Выберете расу вашего персонажа:",reply_markup=races_keyboard)
        await state.set_state(Form.auto_char_race)

@router.callback_query(Form.auto_char_race)
async def enter_char_race(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню с выбором пола персонажа"""
    await callback_query.answer()
    if callback_query.data == 'main_menu':
        await main_menu_query(callback_query)
    else:
        await state.update_data({"race": callback_query.data})
        await callback_query.message.edit_caption(caption="Выберете пол вашего персонажа:",reply_markup=gender_keyboard)
        await state.set_state(Form.auto_char_gender)

@router.callback_query(Form.auto_char_gender)
async def enter_char_gender(callback_query: types.CallbackQuery, state: FSMContext):
    """Создание и вывод автоматически сгенерированного персонажа"""
    await callback_query.answer()
    if callback_query.data == 'main_menu':
        await main_menu_query(callback_query)
    else:
        await state.update_data({"gender": callback_query.data})
        data = await state.get_data()
        response = await auto_create_char({"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]})
        response["user_id"] = callback_query.from_user.id
        await callback_query.message.delete()
        await callback_query.message.answer(text=convert_json_to_char_info(response),parse_mode="MarkdownV2",reply_markup=what_do_next)
        await state.clear()
        await state.update_data({"created_message_id": callback_query.message.message_id})
        await state.update_data({"char" : response})
    
@router.callback_query(lambda c: c.data == 'discard_character')
async def discard_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие подтверждения удаления персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы действительно хотите удалить персонажа?", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.discard_character)
    
@router.callback_query(Form.discard_character)
async def discard_character(callback_query: types.CallbackQuery, state: FSMContext):
    """Удаление или отмена удаления персонажа"""
    await callback_query.answer()
    if callback_query.data == 'yes':
        await callback_query.message.delete()
        await main_menu(callback_query.message,text="Вы жестоко удалили вашего персонажа!")
    else:
        char = await state.get_data()
        char = char["char"]
        await callback_query.message.edit_text(text=f"{convert_json_to_char_info(char)}\nВы отменили удаление персонажа",reply_markup=what_do_next,parse_mode="MarkdownV2")

@router.callback_query(lambda c: c.data == 'save_character')
async def save_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Сохранение сгенерированного персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    char["user_id"] = str(callback_query.from_user.id)
    response = await create_char(char)
    await main_menu_query(callback_query)
    await callback_query.message.edit_caption(caption=f"Ваш персонаж по имени {response['name']} был успешно создан!",reply_markup=main_menu_keyboard)

@router.callback_query(lambda c: c.data == 'update_character')
async def update_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие меню изменения данных персонажа"""
    await callback_query.answer()
    text = await state.get_data()
    text = json.dumps(text["char"],indent=2, ensure_ascii=False)
    await state.update_data({"char": json.loads(text)})
    await callback_query.message.edit_reply_markup(reply_markup=change_character)

@router.callback_query(lambda c: c.data == 'char_name')
async def enter_char_name(callback_query: types.CallbackQuery,state: FSMContext):
    """Ввод нового имени персонажа"""
    await callback_query.answer()
    await callback_query.message.answer(text="Введите имя персонажа:")
    await state.set_state(Form.char_name)

@router.message(Form.char_name)
async def char_name(message: types.Message,state: FSMContext):
    """Установка нового имени персонажа"""
    name = message.text
    char = await state.get_data()
    char = char["char"]
    char["name"] = name
    await message.answer(text=f"Ваш персонаж после правок:\n\n{convert_json_to_char_info(char)}",parse_mode="MarkdownV2",reply_markup=what_do_next)
    await state.clear()
    await state.update_data({"char" : char})

@router.callback_query(lambda c: c.data == 'char_age')
async def enter_char_age(callback_query: types.CallbackQuery,state: FSMContext):
    """Ввод нового возраста персонажа"""
    await callback_query.answer()
    await callback_query.message.answer(text="Введите возраст персонажа:")
    await state.set_state(Form.char_age)

@router.message(Form.char_age)
async def char_age(message: types.Message,state: FSMContext):
    """Изменение возраста персонажа"""
    age = int(message.text)
    char = await state.get_data()
    char = char["char"]
    char["age"] = age
    await message.answer(text=f"Ваш персонаж после правок:\n\n{convert_json_to_char_info(char)}",parse_mode="MarkdownV2",reply_markup=what_do_next)   
    await state.clear()
    await state.update_data({"char" : char})
    
@router.callback_query(lambda c: c.data == 'char_surname')
async def enter_char_surname(callback_query: types.CallbackQuery,state: FSMContext):
    """Ввод новой фамилии персонажа"""
    await callback_query.answer()
    await callback_query.message.answer(text="Введите фамилию персонажа:")
    await state.set_state(Form.char_name)

@router.message(Form.char_surname)
async def char_surname(message: types.Message,state: FSMContext):
    """Изменение фамилии персонажа"""
    surname = message.text
    char = await state.get_data()
    char = char["char"]
    char["surname"] = surname
    await message.answer(text=f"Ваш персонаж после правок:\n\n{convert_json_to_char_info(char)}",parse_mode="MarkdownV2",reply_markup=what_do_next)
    await state.clear()
    await state.update_data({"char" : char})