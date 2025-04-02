import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.character import char_menus_handlers, create_char_handlers, inventory_handlers, main_info_handlers, notes_handlers, spells_handlers, traits_handlers
from handlers import commands_handlers, profile_handlers, session_handlers

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

routers = [
    char_menus_handlers.router,
    create_char_handlers.router,
    inventory_handlers.router,
    main_info_handlers.router,
    notes_handlers.router,
    spells_handlers.router,
    traits_handlers.router,
    commands_handlers.router,
    profile_handlers.router,
    session_handlers.router
]

async def main():
    for router in routers:
        dp.include_router(router)

    print(
        "==============\n"
        "BOT IS WORKING\n"
        "=============="
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())