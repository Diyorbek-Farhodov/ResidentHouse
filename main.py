import asyncio
import os

from aiogram.client.default import DefaultBotProperties
from aiogram import Dispatcher, Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import router
from json_handler import clear_data

load_dotenv()




BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN,  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db = Dispatcher(storage=MemoryStorage())


async def on_startup():
    clear_data()
    print("Bot ishga tushdi")


async def main():
    # clear_all_session()
    db.include_router(router)
    await on_startup()
    await db.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())