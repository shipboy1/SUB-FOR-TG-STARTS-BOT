from aiogram import Bot, Dispatcher
from app.handlers import r
from app.database.models import async_main
from dotenv import find_dotenv, load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage



import os
import asyncio

async def main():
    await async_main()
    load_dotenv(find_dotenv())
    storage = MemoryStorage()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(storage=storage)
    dp.include_router(r)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')

