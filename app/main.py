import asyncio
from aiogram import Bot, Dispatcher


from config import settings
from bot.handlers import router as handlers_router

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

dp.include_router(handlers_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
