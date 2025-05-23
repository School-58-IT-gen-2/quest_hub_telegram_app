from aiogram import types, Router
from aiogram.types import InputMediaPhoto, FSInputFile, CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import random
import aiohttp
import uuid

from keyboards.character_keyboards import *
from keyboards.common_keyboards import *
from server_requests.character_requests.character_requests import *
from forms import Form
from converter import *


router = Router()

# --- Some data for constructor ---
# На самом деле не очень понятно, где эти списки хранить. в handlers не очень, новый файл создавать ради 3 списков тоже не очень.
# Ну пусть будет тут пока
CLASSES = [
    "Варвар",
    "Бард",
    "Плут",
    "Друид",
    "Колдун",
    "Монах",
    "Паладин",
    "Следопыт",
    "Жрец",
    "Чародей",
    "Воин",
    "Колдун"
]

RACES = ["Человек", "Эльф", "Полуорк", "Гном", "Дварф", "Полурослик", "Драконорождённый", "Полуэльф", "Тифлинг"]
GENDERS = ["Мужской", "Женский"]

SUBRACES = {
    "Драконорождённый": ["Красный драконорождённый", "Синий драконорождённый"],
    "Дварф": ["Горный дворф", "Холмовой дворф"],
    "Эльф": ["Высший эльф", "Лесной эльф", "Тёмный эльф (дроу)"],
    "Гном": ["Горный гном", "Лесной гном"],
    "Полуэльф": ["Эльфийский полуэльф", "Человечий полуэльф"],
    "Полурослик": ["Ловкий полурослик", "Стойкий полурослик"]
}

@router.callback_query(Form.regenerate_char)
async def regenerate_char(callback_query: types.CallbackQuery, state: FSMContext):
    """Перегенерация персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == "yes":
        response = await auto_create_char({"gender": char["gender"], "race": char["race"], "character_class": char["character_class"]})
        response["user_id"] = str(callback_query.from_user.id)
        response["name"] = char["name"]
        response["surname"] = char["surname"]
        char = await update_char(response, char["id"])
        await state.update_data({"char": char})
        await callback_query.message.edit_caption(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)
    else:
        await callback_query.message.edit_caption(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)

@router.callback_query(Form.delete_character_confirm)
async def delete_character_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню подтверждения удаления персонажа"""
    await callback_query.answer()
    char = (await state.get_data())["char"]
    if callback_query.data == "yes":
        await delete_char(char["id"])
        await state.clear()
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)
        await callback_query.message.edit_caption(caption="Вы жестоко удалили вашего персонажа!", reply_markup=characters_keyboard)
    if callback_query.data == "no":
        await callback_query.message.edit_caption(parse_mode="MarkdownV2",text=f"{(await character_card(char))['main_char_info']}",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)

@router.callback_query(lambda c: c.data == 'create_character')
async def choose_creation(callback_query: types.CallbackQuery, state: FSMContext):
    """Выбор способа создания персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/char_create.png")))
    await callback_query.message.edit_caption(
        caption="Как вы хотите создать персонажа?\n\n🔹 Быстро — по 3 вопросам\n🔹 Подробно — выбрав все параметры вручную",
        reply_markup=create_method_keyboard
    )

@router.callback_query(lambda c: c.data == 'quick_create')
async def quick_create_start(callback_query: types.CallbackQuery, state: FSMContext):
    """Начало быстрого создания персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_caption(
        caption="Ответьте на три вопроса, а мы заполним все остальное! :)\n\nВыберите класс вашего персонажа:",
        reply_markup=classes_keyboard
    )
    await state.set_state(Form.auto_char_class)

@router.callback_query(lambda c: c.data == 'detailed_create')
async def detailed_create_start(callback_query: types.CallbackQuery, state: FSMContext):
    """Начало подробного создания персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_caption(
        caption="Вы выбрали подробное создание персонажа. Начнем по шагам!\n\nШаг 1: Выберите класс:",
        reply_markup=get_keyboard(CLASSES, add_back=False)
    )
    await state.set_state(Form.CHOOSING_CLASS)




@router.callback_query(Form.CHOOSING_CLASS)
async def choose_class(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "__random__":
        selected = random.choice(CLASSES)
    elif callback.data == "__back__":
        await callback.message.edit_caption(caption="Выберите класс персонажа:", reply_markup=get_keyboard(CLASSES, add_back=False))
        return
    else:
        selected = callback.data

    await state.update_data(char_class=selected)
    await callback.message.edit_caption(caption="Выберите расу персонажа:", reply_markup=get_keyboard(RACES))
    await state.set_state(Form.CHOOSING_RACE)

@router.callback_query(Form.CHOOSING_RACE)
async def choose_race(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "__random__":
        selected = random.choice(RACES)
    elif callback.data == "__back__":
        await callback.message.edit_caption(caption="Выберите класс персонажа:", reply_markup=get_keyboard(CLASSES))
        await state.set_state(Form.CHOOSING_CLASS)
        return
    else:
        selected = callback.data

    await state.update_data(char_race=selected)

    if selected in SUBRACES:
        await callback.message.edit_caption(caption=f"Выберите подрасу для {selected}:", reply_markup=get_keyboard(SUBRACES[selected]))
        await state.set_state(Form.CHOOSING_SUBRACE)
    else:
        await callback.message.edit_caption(caption="Выберите гендер персонажа:", reply_markup=get_keyboard(GENDERS))
        await state.set_state(Form.CHOOSING_GENDER)

@router.callback_query(Form.CHOOSING_SUBRACE)
async def choose_subrace(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    race = user_data.get("char_race")

    if callback.data == "__random__":
        selected = random.choice(SUBRACES[race])
    elif callback.data == "__back__":
        await callback.message.edit_caption(caption="Выберите расу персонажа:", reply_markup=get_keyboard(RACES))
        await state.set_state(Form.CHOOSING_RACE)
        return
    else:
        selected = callback.data

    await state.update_data(char_subrace=selected)
    await callback.message.edit_caption(caption="Выберите гендер персонажа:", reply_markup=get_keyboard(GENDERS))
    await state.set_state(Form.CHOOSING_GENDER)

@router.callback_query(Form.CHOOSING_GENDER)
async def choose_gender(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "__random__":
        selected = random.choice(GENDERS)
    elif callback.data == "__back__":
        user_data = await state.get_data()
        race = user_data.get("char_race")
        if race in SUBRACES:
            await callback.message.edit_caption(caption=f"Выберите подрасу для {race}:", reply_markup=get_keyboard(SUBRACES[race]))
            await state.set_state(Form.CHOOSING_SUBRACE)
        else:
            await callback.message.edit_caption(caption="Выберите расу персонажа:", reply_markup=get_keyboard(RACES))
            await state.set_state(Form.CHOOSING_RACE)
        return
    else:
        selected = callback.data

    await state.update_data(char_gender=selected)
    data = await state.get_data()

    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/character-list-options", params=data) as resp:
            if resp.status == 200:
                json_data = await resp.json()
                json_data['inventory'] = list(filter(lambda x: isinstance(x, list), json_data['inventory']))
                await state.update_data(
                    json_data=json_data,
                    characteristics_options=json_data["options"],
                    current_stat_index=0
                )

                # Второй запрос: инициализация персонажа
                init_payload = {
                    "user_id": str(callback.from_user.id),
                    "gender": data.get("char_gender"),
                    "character_class": data.get("char_class"),
                    "race": data.get("char_race"),
                    "subrace": data.get("char_subrace", "random")
                }

                async with session.post("http://localhost:8000/initialize-character-list", json=init_payload) as post_resp:
                    if post_resp.status == 200:
                        init_response = await post_resp.json()
                        await state.update_data(character_list=init_response)
                    else:
                        await callback.message.answer("Ошибка при инициализации персонажа.")



                await ask_next_stat(callback.message, state)
                await state.set_state(Form.SETTING_CHARACTERISTIC)
            else:
                await callback.message.edit_caption(caption="Произошла ошибка при получении данных с сервера.")

async def ask_next_stat(message: Message, state: FSMContext):
    data = await state.get_data()
    stat_names = list(data["characteristics_options"].keys())
    index = data["current_stat_index"]
    if index >= len(stat_names):
        await state.set_state(Form.CHOOSING_SKILLS)
        await start_skills_selection(message, state)
        return

    stat = stat_names[index]
    all_values = data["characteristics_options"][stat][0]
    recommended = set(data["characteristics_options"][stat][1])
    display_values = [
        f"{val} 🌟" if val in recommended else val for val in all_values
    ]
    keyboard = get_keyboard(display_values)
    await message.edit_caption(caption=f"Выберите значение для характеристики *{stat}*:", reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(Form.SETTING_CHARACTERISTIC)
async def set_characteristic(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    stat_names = list(data["characteristics_options"].keys())
    index = data["current_stat_index"]
    stat = stat_names[index]

    if callback.data == "__random__":
        selected = random.choice(data["characteristics_options"][stat][0])
    elif callback.data == "__back__":
        if index == 0:
            await callback.message.edit_caption(caption="Выберите гендер персонажа:", reply_markup=get_keyboard(GENDERS))
            await state.set_state(Form.CHOOSING_GENDER)
            return
        await state.update_data(current_stat_index=index - 1)
        await ask_next_stat(callback.message, state)
        return
    else:
        selected = callback.data.replace(" 🌟", "")  # удаляем пометку рекомендации

    stats = data.get("char_stats", {})
    stats[stat] = selected
    await state.update_data(char_stats=stats, current_stat_index=index + 1)
    await ask_next_stat(callback.message, state)

async def start_skills_selection(message: Message, state: FSMContext):
    data = await state.get_data()
    skills = data["json_data"]["skils"]
    skills_list = skills["skills_list"]
    limit = skills["skills_limit"]
    await state.update_data(skills_selected=[], skills_limit=limit)
    await ask_next_skill(message, state)

async def ask_next_skill(message: Message, state: FSMContext):
    data = await state.get_data()
    selected = set(data["skills_selected"])
    skills_list = [s for s in data["json_data"]["skils"]["skills_list"] if s not in selected]
    limit = data["skills_limit"]

    if len(selected) >= limit:
        await message.edit_caption(caption=f"Вы выбрали все {limit} навыков: {', '.join(selected)}")
        await state.set_state(Form.SELECTING_INVENTORY_ITEM)
        await state.update_data(current_inventory_index=0, inventory_selected=[])
        await ask_inventory_item(message, state)

        return

    keyboard = get_keyboard(skills_list)
    await message.edit_caption(caption=f"Выберите навык ({len(selected) + 1} из {limit}):", reply_markup=keyboard)

@router.callback_query(Form.CHOOSING_SKILLS)
async def choose_skill(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    selected = data["skills_selected"]
    limit = data["skills_limit"]
    all_skills = data["json_data"]["skils"]["skills_list"]

    if callback.data == "__random__":
        remaining = [s for s in all_skills if s not in selected]
        selected_skill = random.choice(remaining)
    elif callback.data == "__back__":
        if not selected:
            # Возврат к характеристикам
            stat_keys = list(data["characteristics_options"].keys())
            await state.update_data(current_stat_index=len(stat_keys)-1)
            await state.set_state(Form.SETTING_CHARACTERISTIC)
            await ask_next_stat(callback.message, state)
            return
        selected.pop()
        await state.update_data(skills_selected=selected)
        await ask_next_skill(callback.message, state)
        return
    else:
        selected_skill = callback.data

    if selected_skill not in selected:
        selected.append(selected_skill)

    await state.update_data(skills_selected=selected)
    await ask_next_skill(callback.message, state)


async def ask_inventory_item(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["current_inventory_index"]
    inventory = data["json_data"]["inventory"]

    if index >= len(inventory):
        selected_items = data["inventory_selected"]
        flat_items = [", ".join(items) for items in selected_items]
        await message.edit_caption(caption=f"Вы выбрали инвентарь:\n" + "\n".join(flat_items))
        await ask_age(message, state)
        return


    options = inventory[index]
    display = [", ".join(option) for option in options]
    keyboard = get_keyboard(display)
    await message.edit_caption(caption=f"Выберите вариант инвентаря ({index+1} из {len(inventory)}):", reply_markup=keyboard)

@router.callback_query(Form.SELECTING_INVENTORY_ITEM)
async def choose_inventory_item(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    index = data["current_inventory_index"]
    inventory = data["json_data"]["inventory"]
    selected_items = data["inventory_selected"]

    if callback.data == "__random__":
        choice = random.choice(inventory[index])
    elif callback.data == "__back__":
        if index == 0:
            await state.set_state(Form.CHOOSING_SKILLS)
            await ask_next_skill(callback.message, state)
            return
        await state.update_data(current_inventory_index=index - 1)
        selected_items.pop()
        await state.update_data(inventory_selected=selected_items)
        await ask_inventory_item(callback.message, state)
        return
    else:
        choice = callback.data.split(", ")

    selected_items.append(choice)
    await state.update_data(inventory_selected=selected_items, current_inventory_index=index + 1)
    await ask_inventory_item(callback.message, state)


async def ask_age(message: Message, state: FSMContext):
    data = await state.get_data()
    age_limits = data["json_data"].get("default_age", {"min": 16, "max": 100})
    min_age = age_limits["min"]
    max_age = age_limits["max"]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайный возраст")],
            # [KeyboardButton(text="⬅️ Назад")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(f"Введите возраст персонажа (от {min_age} до {max_age}):", reply_markup=keyboard)
    await state.set_state(Form.CHOOSING_AGE)

@router.message(Form.CHOOSING_AGE)
async def handle_age_input(message: Message, state: FSMContext):
    data = await state.get_data()
    age_limits = data["json_data"].get("default_age", {"min": 16, "max": 100})
    min_age = age_limits["min"]
    max_age = age_limits["max"]

    if message.text == "⬅️ Назад":
        await state.set_state(Form.SELECTING_INVENTORY_ITEM)
        await ask_inventory_item(message, state)
        return

    if message.text == "🎲 Случайный возраст":
        age = random.randint(min_age, max_age)
        await state.update_data(char_age=age)
        await message.answer(f"Случайный возраст выбран: {age}", reply_markup=ReplyKeyboardRemove())
        await ask_story(message, state)
        return

    try:
        age = int(message.text)
        if not (min_age <= age <= max_age):
            raise ValueError
    except ValueError:
        await message.answer(f"Пожалуйста, введите число от {min_age} до {max_age}.")
        return

    await state.update_data(char_age=age)
    await message.answer(f"Возраст установлен: {age}", reply_markup=ReplyKeyboardRemove())
    await ask_story(message, state)


async def ask_story(message: Message, state: FSMContext):
    data = await state.get_data()
    stories = data["json_data"].get("default_story", ["Без истории"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайная предыстория")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Введите предысторию персонажа или выберите случайную:", reply_markup=keyboard)
    await state.set_state(Form.CHOOSING_STORY)

@router.message(Form.CHOOSING_STORY)
async def handle_story_input(message: Message, state: FSMContext):
    data = await state.get_data()
    stories = data["json_data"].get("default_story", [])

    if message.text == "🎲 Случайная предыстория":
        selected_story = random.choice(stories)
        await message.answer(f"Случайная предыстория выбрана:\n\n{selected_story}", reply_markup=ReplyKeyboardRemove())
    else:
        selected_story = message.text
        await message.answer("Предыстория установлена.", reply_markup=ReplyKeyboardRemove())

    await state.update_data(char_story=selected_story)

    await ask_name(message, state)


async def ask_name(message: Message, state: FSMContext):
    data = await state.get_data()
    default_names = data["json_data"].get("default_names", ["Имя неизвестно"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайное имя")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Введите имя персонажа или выберите случайное:", reply_markup=keyboard)
    await state.set_state(Form.CHOOSING_NAME)

@router.message(Form.CHOOSING_NAME)
async def handle_name_input(message: Message, state: FSMContext):
    data = await state.get_data()
    names = data["json_data"].get("default_names", [])

    if message.text == "🎲 Случайное имя":
        selected_name = random.choice(names) if names else "Имя неизвестно"
        await message.answer(f"Случайное имя выбрано: {selected_name}", reply_markup=ReplyKeyboardRemove())
    else:
        selected_name = message.text
        await message.answer(f"Имя установлено: {selected_name}", reply_markup=ReplyKeyboardRemove())

    await state.update_data(char_name=selected_name)

    # Здесь можно завершить создание или вывести резюме
    await message.answer("Персонаж успешно создан! 🎉")
    await show_character_summary(message, state)


async def show_character_summary(message: Message, state: FSMContext):
    data = await state.get_data()

    race = data.get("char_race", "—")
    subrace = data.get("char_subrace")
    if subrace:
        race = f"{race} ({subrace})"

    characteristics = "\n".join([f"- *{k}*: {v}" for k, v in data.get("char_stats", {}).items()])
    skills = ", ".join(data.get("skills_selected", []))
    inventory = "\n".join([f"- {', '.join(i)}" for i in data.get("inventory_selected", [])])
    story = data.get("char_story", "—")
    name = data.get("char_name", "—")

    character_list = data.get('character_list')
    

    character_list['stats']['strength'] = data.get("char_stats")['Сила']
    character_list['stats']['dexterity'] = data.get("char_stats")['Ловкость']
    character_list['stats']['constitution'] = data.get("char_stats")['Телосложение']
    character_list['stats']['intelligence'] = data.get("char_stats")['Интеллект']
    character_list['stats']['wisdom'] = data.get("char_stats")['Мудрость']
    character_list['stats']['charisma'] = data.get("char_stats")['Харизма']

    character_list['skills'] = data.get("skills_selected")

    for i in data.get('inventory_selected'):
        character_list['inventory'].append({
            'id': str(uuid.uuid4()),
            'count': 1,
            'name': i,
            'description': 'Без описания'
        })

    character_list['backstory'] = data.get("char_story")

    character_list['name'] = data.get("char_name")

    character_list['age'] = data.get("char_age")

    print(character_list)

    async with aiohttp.ClientSession() as session:
        async with session.put("http://localhost:8000/save-character-list", json=character_list) as post_resp:
            if post_resp.status == 200:
                print(post_resp)
            else:
                print(post_resp.json)
                print(post_resp)
                print(post_resp.status)
                init_response = await post_resp.json()
                print(init_response)
                print('API вернул ошибку')




    text = (
        f"*🧝‍♂️ Лист персонажа:*\n"
        f"*Имя:* {name}\n"
        f"*Класс:* {data.get('char_class', '—')}\n"
        f"*Раса:* {race}\n"
        f"*Пол:* {data.get('char_gender', '—')}\n"
        f"*Возраст:* {data.get('char_age', '—')}\n\n"
        f"*📊 Характеристики:*\n{characteristics}\n\n"
        f"*🎯 Навыки:*\n{skills}\n\n"
        f"*🎒 Инвентарь:*\n{inventory}\n\n"
        f"*📖 Предыстория:*\n_{story}_"
    )

    await message.answer(text, parse_mode="Markdown")






@router.callback_query(Form.auto_char_class)
async def enter_char_class(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню с выбором расы персонажа"""
    await callback_query.answer()
    if callback_query.data == 'char_back':
        await state.clear()
        await callback_query.message.edit_media(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard)
    else:
        await state.update_data({"character_class": callback_query.data})
        await callback_query.message.edit_caption(caption="Выберете расу вашего персонажа:",reply_markup=races_keyboard)
        await state.set_state(Form.auto_char_race)

@router.callback_query(Form.auto_char_race)
async def enter_char_race(callback_query: types.CallbackQuery, state: FSMContext):
    """Открытие меню с выбором пола персонажа"""
    await callback_query.answer()
    if callback_query.data == 'char_back':
        await callback_query.message.edit_caption(caption="Ответьте на три вопроса, а мы заполним все остальное! :)\n\nВыберите класс вашего персонажа:",  reply_markup=classes_keyboard)
        await state.set_state(Form.auto_char_class)
    else:
        await state.update_data({"race": callback_query.data})
        await callback_query.message.edit_caption(caption="Выберете пол вашего персонажа:",reply_markup=gender_keyboard)
        await state.set_state(Form.auto_char_gender)

@router.callback_query(Form.auto_char_gender)
async def enter_char_gender(callback_query: types.CallbackQuery, state: FSMContext):
    """Создание и вывод автоматически сгенерированного персонажа"""
    await callback_query.answer()
    if callback_query.data == 'char_back':
        await callback_query.message.edit_caption(caption="Выберете расу вашего персонажа:",reply_markup=races_keyboard)
        await state.set_state(Form.auto_char_race)
    else:
        gender = callback_query.data
        await state.update_data({"gender": gender})
        data = await state.get_data()
        response = await auto_create_char({"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]})
        response["user_id"] = str(callback_query.from_user.id)
        char  = await create_char(response)
        await callback_query.message.delete()
        await callback_query.message.answer(text=(await character_card(char))["main_char_info"],parse_mode="MarkdownV2",reply_markup=character_card_keyboard)
        await state.set_state(Form.character_card)
        await state.update_data({"char": char})
        await state.update_data({"base_char_info" : {"gender": data["gender"], "race": data["race"], "character_class": data["character_class"]}})
    
@router.callback_query(lambda c: c.data == 'discard_character')
async def discard_character(callback_query: types.CallbackQuery,state: FSMContext):
    """Открытие подтверждения удаления персонажа"""
    await callback_query.answer()
    await callback_query.message.edit_caption(text="Удалённого персонажа *невозможно восстановить*\. Продолжить\?", reply_markup=yes_or_no_keyboard,parse_mode="MarkdownV2")
    await state.set_state(Form.discard_character)
    
@router.callback_query(Form.discard_character)
async def discard_character(callback_query: types.CallbackQuery, state: FSMContext):
    """Удаление или отмена удаления персонажа"""
    await callback_query.answer()
    char = await state.get_data()
    char_id = char["char"]["id"]
    if callback_query.data == 'yes':
        await delete_char(char_id)
        await callback_query.message.delete()
        await state.clear()
        await callback_query.message.answer_photo(media=InputMediaPhoto(media=FSInputFile("assets/characters.png")), reply_markup=characters_keyboard, caption="Вы жестоко удалили вашего персонажа!")
    else:
        char = await state.get_data()
        base_info = char["base_char_info"]
        char = char["char"]
        await state.update_data({"base_char_info" : base_info})
        await state.update_data({"char" : char})
        await callback_query.message.delete()
        await state.set_state(Form.main_char_info_menu)
        await callback_query.message.answer(text=f"{(await character_card(char))['main_char_info']}",reply_markup=character_card_keyboard,parse_mode="MarkdownV2")
