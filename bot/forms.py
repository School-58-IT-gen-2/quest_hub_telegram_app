from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    delete_profile_confirm = State()
    get_user_age = State()

    delete_character_confirm = State()
    discard_character = State()
    view_character = State()
    auto_char_class = State()
    auto_char_race = State()
    auto_char_gender = State()
    regenerate_char = State()

    character_card = State()

    char_name = State()
    char_age = State()
    change_char_name = State()
    change_char_age = State()
    change_char_surname = State()

    inventory_menu = State()
    items_menu = State()
    ammunition_menu = State()
    gold_menu = State()
    change_gold = State()
    change_xp = State()
    ammunition_item_menu = State()
    change_ammunition_item_name = State()
    change_ammunition_item_desc = State()
    inventory_item_menu = State()
    change_inventory_item_name = State()
    change_inventory_item_desc = State()

    main_char_info_menu = State()
    name_menu = State()
    age_menu = State()
    backstory_menu = State()
    languages_menu = State()
    experience_menu = State()
    lvl_menu = State()
    change_backstory = State()
    add_language = State()
    delete_language = State()
    language_menu = State()
    
    spells_menu = State()

    notes_menu = State()
    note_menu = State()
    change_note_title = State()
    change_note_text = State()
    create_note_title = State()
    create_note_text = State()
    delete_note = State()

    traits_menu = State()
    trait_menu = State()
    change_trait_name = State()
    change_trait_description = State()
    create_trait_name = State()
    create_trait_description = State()
    delete_trait = State()
    
    choose_game_action = State()
    game_type_menu = State()
    open_game_menu = State()
    private_game_menu = State()
    game_format_menu = State()
    game_level_menu = State()
    game_name_menu = State()
    game_city_menu = State()
    game_player_count_menu = State()
    game_description_menu = State()
    game_ready = State()
    game_params_menu = State()
    game_filters_menu = State()
    game_seed_menu = State()
    join_game_menu = State()
    create_char_game_menu = State()
    choose_char_menu = State()
    game_send_char_menu = State()
    choose_game_menu = State()
    connect_game_chat = State()