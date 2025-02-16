import asyncio
import json
import random

from aiogram import Dispatcher, types, Router
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests import *
from handlers.commands import main_menu, main_menu_query
from forms import Form
from converter import character_card


dp = Dispatcher()
router = Router()

@router.callback_query(lambda c: c.data == 'characters')
async def characters(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню персонажей"""
    await callback_query.answer()
    await state.clear()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)

@router.callback_query(lambda c: c.data == 'view_characters')
async def view_characters(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие списка всех персонажей пользователя"""
    await callback_query.answer()
    await state.clear()
    user_chars = await get_char_by_user_id(callback_query.from_user.id)
    if len(user_chars) == 0:
        await callback_query.message.edit_caption(caption="У вас ещё нет персонажей", reply_markup=characters_keyboard)
    else:
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=await build_char_kb(user_chars, 0))
        await state.set_state(Form.view_character)

@router.callback_query(Form.view_character)
async def view_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Вывод персонажа"""
    await callback_query.answer()
    if 'char_left' in callback_query.data or 'char_right' in callback_query.data:
        user_chars = await get_char_by_user_id(callback_query.from_user.id)
        page = int(callback_query.data.split('_')[-1])
        direction = -1 if callback_query.data.split('_')[-2] == 'left' else 1
        if -1 < page + direction < -(-len(user_chars) // 6):
            await callback_query.message.edit_caption(reply_markup=await build_char_kb(user_chars, page + direction))
    else:
        char = await get_char_by_char_id(int(callback_query.data))
        char = char[0]
        await callback_query.message.delete()
        await callback_query.message.answer(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)
        await state.update_data({"char": char})

@router.callback_query(Form.character_card)
async def view_char_params(callback_query: types.CallbackQuery, state: FSMContext):
    """Вывод отдельных параметров песонажа персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "inventory":
        await callback_query.message.edit_text(text='🎒 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    if callback_query.data == "traits":
        await callback_query.message.edit_text(text=character_card(char)["traits_and_abilities"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.traits_menu)
    if callback_query.data == "main_char_info":
        await callback_query.message.edit_text(text='👤 *_Основные параметры:_*', reply_markup=main_char_info_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.main_char_info_menu)

@router.callback_query(Form.main_char_info_menu)
async def main_char_info_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Основные сведения о персонаже"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "name":
        await callback_query.message.edit_text(text=character_card(char)["inventory"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.items_menu)
    if callback_query.data == "age":
        await callback_query.message.edit_text(text=character_card(char)["ammunition"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.ammunition_menu)
    if callback_query.data == "backstory":
        pass
    if callback_query.data == "languages":
        pass
    if callback_query.data == "back":
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.traits_menu)
async def traits_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Черты и особенности персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.inventory_menu)
async def inventory(callback_query: types.CallbackQuery, state: FSMContext):
    """Инвентарь персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    if callback_query.data == "items":
        await callback_query.message.edit_text(text=character_card(char)["inventory"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.items_menu)
    if callback_query.data == "ammunition":
        await callback_query.message.edit_text(text=character_card(char)["ammunition"], reply_markup=edit_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.ammunition_menu)
    if callback_query.data == "exp":
        pass
    if callback_query.data == "gold":
        pass
    if callback_query.data == "back":
        await callback_query.message.edit_text(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard) 
        await state.set_state(Form.character_card)

@router.callback_query(Form.items_menu)
async def items_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Предметы персонажа"""
    await callback_query.answer()
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='🎒 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)

@router.callback_query(Form.ammunition_menu)
async def ammunition_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Амуниция персонажа"""
    await callback_query.answer()
    if callback_query.data == 'back':
        await callback_query.message.edit_text(text='🎒 *_Инвентарь:_*', reply_markup=inventory_keyboard,parse_mode="MarkdownV2")
        await state.set_state(Form.inventory_menu)
    

@router.callback_query(lambda c: c.data == 'regenerate_character_from_put')
async def regenerate_character_from_put(callback_query: types.CallbackQuery, state: FSMContext):
    """активация state для изменения персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы уверены в том, что хотите перегенерировать персонаж? Весь ваш прогресс на персонаже при этом будет утерян.", reply_markup=yes_or_no_keyboard)
    await state.set_state(Form.regenerate_char)

@router.callback_query(Form.regenerate_char)
async def regenerate_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Перегенерация персонажа"""
    await callback_query.answer()
    if callback_query.data == "yes":
        await callback_query.answer()
        char = await state.get_data()
        char = char["char"]
        gender = "M" if random.random() < 0.5 else "W"
        new_char = await auto_create_char({"character_class": char["character_class"], "race": char["race"], "gender": gender})
        try:
            await delete_char(char["id"])
            new_char["user_id"] = char["user_id"]
            await create_char(new_char)
        except:
            pass
        new_char["user_id"] = char["user_id"]
        await callback_query.message.edit_text(text=character_card(new_char)["main_char_info"],reply_markup=change_or_delete_character,parse_mode="MarkdownV2")
        await state.update_data({"char": new_char})
        await state.update_data({"base_char_info": {"character_class": char["character_class"], "race": char["race"], "gender": gender}})
    else:
        char = await state.get_data()
        base_info = char["base_char_info"]
        char = char["char"]
        await state.update_data({"base_char_info" : base_info})
        await state.update_data({"char" : char})
        await callback_query.message.delete()
        await callback_query.message.answer(text=f"{character_card(char)["main_char_info"]}\n\nВы отменили перегенерацию персонажа персонажа",reply_markup=change_or_delete_character,parse_mode="MarkdownV2")

@router.callback_query(lambda c: c.data == 'put_character')
async def put_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Обновление данных персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=put_change_character)
    
@router.callback_query(lambda c: c.data == 'back_to_char_from_put')
async def back_to_char_from_put(callback_query: types.CallbackQuery, state: FSMContext):
    """Выход из меню изменения персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=change_or_delete_character)

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
    await message.answer(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=change_or_delete_character)
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
    await message.answer(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=change_or_delete_character)
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
    await message.answer(text=character_card(char)["main_char_info"],parse_mode="MarkdownV2",reply_markup=change_or_delete_character)
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
        await callback_query.message.edit_text(parse_mode="MarkdownV2",text=f"{character_card(char["main_char_info"])}\n\nВы отказались от удаления персонажа",reply_markup=change_or_delete_character)

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
        gender = callback_query.data
        await state.update_data({"gender": gender})
        data = await state.get_data()
        response = await auto_create_char({"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]})
        response["user_id"] = callback_query.from_user.id
        await callback_query.message.delete()
        await callback_query.message.answer(text=character_card(response),parse_mode="MarkdownV2",reply_markup=what_do_next)
        await state.clear()
        response["gender"] = gender
        await state.update_data({"char" : response})
        await state.update_data({"base_char_info" : {"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]}})
    
@router.callback_query(lambda c: c.data == 'discard_character')
async def discard_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие подтверждения удаления персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_text(text="Вы действительно хотите удалить персонажа?", reply_markup=yes_or_no_keyboard)
    #print(await state.get_data())
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
        base_info = char["base_char_info"]
        char = char["char"]
        await state.update_data({"base_char_info" : base_info})
        await state.update_data({"char" : char})
        await callback_query.message.delete()
        await callback_query.message.answer(text=f"{character_card(char)["main_char_info"]}\n\nВы отменили удаление персонажа",reply_markup=what_do_next,parse_mode="MarkdownV2")

@router.callback_query(lambda c: c.data == 'save_character')
async def save_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Сохранение сгенерированного персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["char"]
    char["user_id"] = str(callback_query.from_user.id)
    response = await create_char(char)
    await characters(callback_query, state)
    await callback_query.message.edit_caption(caption=f"Ваш персонаж по имени {response['name']} был успешно создан!",reply_markup=characters_keyboard)

@router.callback_query(lambda c: c.data == 'regenerate_character')
async def regenerate_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Перегенерация персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char = char["base_char_info"]
    response = await auto_create_char({"gender": char["gender"], "race": char["race"], "character_class": char["character_class"]})
    response["user_id"] = callback_query.from_user.id
    await callback_query.message.edit_text(text=f"Ваш новый персонаж:\n\n{character_card(response)["main_char_info"]}",parse_mode="MarkdownV2",reply_markup=what_do_next)
    
@router.callback_query(lambda c: c.data == 'back_to_char_from_generation')
async def back_to_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Возвращение к персонажу"""
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=what_do_next)

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
    await message.answer(text=f"Ваш персонаж после правок:\n\n{character_card(char)["main_char_info"]}",parse_mode="MarkdownV2",reply_markup=what_do_next)
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
    await message.answer(text=f"Ваш персонаж после правок:\n\n{character_card(char)["main_char_info"]}",parse_mode="MarkdownV2",reply_markup=what_do_next)   
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
    await message.answer(text=f"Ваш персонаж после правок:\n\n{character_card(char)["main_char_info"]}",parse_mode="MarkdownV2",reply_markup=what_do_next)
    await state.clear()
    await state.update_data({"char" : char})