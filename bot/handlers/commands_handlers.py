from aiogram import Dispatcher, types, Router, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import *
from server_requests.profile_requests import *
from converter import *


router = Router()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    """Вывод приветствия и создание пользователя"""
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
    await state.clear()
    message_text = f"Добро пожаловать, {message.from_user.first_name}!\nБолее известный в Фаэруне как {message.from_user.username}."
    await create_user(user_data)
    await message.answer_photo(caption=message_text,photo=FSInputFile("assets/main_menu.png"), reply_markup=main_menu_keyboard)

@router.message(Command("help"))
async def help(message: types.Message):
    """Вывод помощи"""
    char = {'race': 'Дварф', 'character_class': 'Следопыт', 'backstory': 'С детства этот дварф был увлечён созданием удивительных вещей — от оружия до механизмов. Он отправился в путь, чтобы изучать новые технологии и ремёсла других народов. Его цель — создать шедевр, который станет легендарным для всех рас.', 'hp': 10, 'initiative': 0, 'lvl': 525252, 'passive_perception': 12, 'speed': 25, 'experience': 0, 'ownership_bonus': 2, 'death_saving_throws': 0, 'interference': False, 'advantages': False, 'weapons_and_equipment': [{'id': '63b7385d-04b3-4f3f-8af9-d31ddadd25a6', 'count': 1, 'type': 'Военное ближнее', 'name': 'Боевой молот', 'weight': 6, 'cost': 10, 'damage': '1d8', 'damage_type': 'Дробящий', 'properties': ['Универсальное (1d10)']}, {'id': '22bc58ab-cbfb-45e7-a360-b1a36eb7aee2', 'count': 1, 'type': 'Средний', 'name': 'Чешуйчатый доспех', 'weight': 45, 'cost': 50, 'ac_base': 14, 'dex_bonus': True, 'max_dex_bonus': 2, 'stealth_disadvantage': True}], 'spells': [], 'traits_and_abilities': [{'id': '8d53a928-3e07-45af-9bf1-95700c32e4ca', 'name': 'Тёмное зрение', 'description': 'Привыкшие к жизни под землей, вы обладаете превосходным зрением в темноте и при тусклом свете. Вы можете видеть в тусклом свете на расстоянии до 60 футов, как при ярком свете, и в полной темноте, как при тусклом свете. Вы не различаете цвета в темноте, видя только оттенки серого.'}, {'id': '4c2c56b8-f642-42ee-9e36-0ce6a171edce', 'name': 'Дворфийская стойкость', 'description': 'Вы имеете преимущество на спасброски от яда и сопротивление к урону ядом.'}, {'id': 'ed3ed521-e8c0-43a9-94a2-e609df0bd034', 'name': 'Дворфийская боевая подготовка', 'description': 'Вы обладаете мастерством в боевом топоре, ручном топоре, лёгком молоте и боевом молоте.'}, {'id': '8de066ff-0b19-40e2-8cd5-dca7e6eda894', 'name': 'Мастерство в инструментах', 'description': 'Вы получаете мастерство в одном из следующих наборов инструментов: кузнечные инструменты, пивоваренное оборудование или каменщик.'}, {'id': '3314f020-8b92-4cce-a9f2-c80e40d2ed79', 'name': 'Чувство камня', 'description': 'Когда вы делаете проверку Истории, связанную с каменной кладкой, вы считаете себя мастером этого навыка и добавляете удвоенный бонус мастерства вместо обычного.'}, {'id': 'a4e7c9f2-4098-4237-a6ea-9185007de4f3', 'name': 'Дворфийская выносливость', 'description': 'Ваш максимальный запас очков здоровья увеличивается на 1, и увеличивается на 1 при каждом уровне.'}], 'languages': ['Общий', 'Дворфийский'], 'special_features': {}, 'weaknesses': {}, 'npc_relations': {}, 'name': 'Адрик', 'skills': ['Внимание', 'Атлетика', 'Выживание', 'Природа', 'Анализ', 'Скрытность', 'Акробатика'], 'stat_modifiers': {'strength': 1, 'dexterity': 2, 'constitution': 0, 'intelligence': 1, 'wisdom': 2, 'charisma': 1}, 'stats': {'strength': 12, 'dexterity': 15, 'constitution': 10, 'intelligence': 12, 'wisdom': 14, 'charisma': 13}, 'user_id': '1648778328', 'inspiration': False, 'surname': 'Вистра', 'inventory': [{'id': '2a0e236a-ec83-416f-aeda-dd087e7d2fa7', 'count': 1, 'name': 'Рюкзак', 'description': 'крутой итем!!!'}, {'id': 'a8c50635-9268-4032-974f-790ad061c7d5', 'count': 1, 'name': 'Спальный мешок', 'description': 'крутой итем!!!'}, {'id': '77a9f6cf-c92b-490c-b3b6-7d67ff7b6ab3', 'count': 1, 'name': 'Мешок для еды на 10 дней', 'description': 'крутой итем!!!'}, {'id': '5cc67d30-999a-4191-b274-e55f9a5f9413', 'count': 1, 'name': 'Кремень и огниво', 'description': 'крутой итем!!!'}, {'id': '7d6a35ca-844e-4bb3-90ec-6c1c85b2c094', 'count': 1, 'name': 'Веревка (50 футов)', 'description': 'крутой итем!!!'}, {'id': 'f7b614b5-0cdc-436c-99a2-da175fb22650', 'count': 1, 'name': 'Фляга', 'description': 'крутой итем!!!'}, {'id': '24338dd2-0352-4797-8f9c-a96dc26336eb', 'count': 1, 'name': 'Пивоваренное оборудование', 'description': 'крутой итем!!!'}], 'age': 203, 'ability_saving_throws': {'strength': 1, 'dexterity': 2}, 'worldview': 'Нейтральный добрый', 'notes': None, 'gold': 0, 'subrace': 'Горный дворф', 'gender': 'M', 'archetype': None, 'id': '57590cae-57d5-46a1-a0ce-c6260bfd0511', 'fighting_style': None, 'created_at': '2025-04-09T17:59:29.673402+00:00', 'diary': None, 'class_features': None, 'valuables': None, 'attack_and_damage_values': None, 'travel_speed': None}
    await message.answer(text=(await game_character_card(char)), parse_mode="MarkdownV2")

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
