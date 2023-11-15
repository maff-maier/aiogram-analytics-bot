import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers import router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router=router)

    # Удаляем все сообщения, которые пришли в момент, когда бот был инактив.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
