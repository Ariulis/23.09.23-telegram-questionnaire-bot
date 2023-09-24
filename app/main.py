import asyncio
from aiogram import Dispatcher


from utils import bot
from bot.handlers import router as handlers_router


dp = Dispatcher()

dp.include_router(handlers_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
