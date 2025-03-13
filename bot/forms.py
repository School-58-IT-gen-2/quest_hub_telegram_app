from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    delete_profile_confirm = State()
    delete_character_confirm = State()
    discard_character = State()
    get_user_age = State()
    view_character = State()
    auto_char_class = State()
    auto_char_race = State()
    auto_char_gender = State()
    char_name = State()
    char_age = State()
    change_char_name = State()
    change_char_age = State()
    change_char_surname = State()
    regenerate_char = State()
    character_card = State()
    inventory_menu = State()
    items_menu = State()
    ammunition_menu = State()
    traits_menu = State()
    main_char_info_menu = State()
    name_menu = State()
    age_menu = State()
    backstory_menu = State()
    languages_menu = State()
    experience_menu = State()
    lvl_menu = State()
    spells_menu = State()
    gold_menu = State()
    change_gold = State()
    change_xp = State()
    ammunition_item_menu = State()
    change_ammunition_item_name = State()
    change_ammunition_item_desc = State()
    inventory_item_menu = State()
    change_inventory_item_name = State()
    change_inventory_item_desc = State()
    notes_menu = State()
    note_menu = State()
    change_note_title = State()
    change_note_text = State()
    create_note_title = State()
    create_note_text = State()
    delete_note = State()
