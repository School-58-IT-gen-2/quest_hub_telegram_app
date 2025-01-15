import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

from keyboards import *
from server_requests import *
from handlers import character, commands, profile, session


load_dotenv()
logging.basicConfig(level=logging.INFO)

<<<<<<< HEAD
=======

>>>>>>> 603cedb1e1fe5f189c0626ecf3752f81ae7a2410
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

async def main():
    dp.include_router(character.router)
    dp.include_router(commands.router)
    dp.include_router(profile.router)
    dp.include_router(session.router)

    print(
        "==============\n"
        "BOT IS WORKING\n"
        "=============="
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())