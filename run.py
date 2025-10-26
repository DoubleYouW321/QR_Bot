import asyncio

import logging as log
from aiogram import Bot, Dispatcher
from app.handlers import router
import os

try:
    from config import TOKEN
except ImportError:
    TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')