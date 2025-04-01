import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

from keyboards import *
from server_requests import *
from handlers.character import char_tab, create_char, inventory, main_info, notes, spells, traits
from handlers import commands, profile, session


load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

routers = [char_tab.router, create_char.router, inventory.router, main_info.router, notes.router, spells.router, traits.router, commands.router, profile.router, session.router]

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