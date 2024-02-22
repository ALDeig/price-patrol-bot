import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from settings import settings


logger = logging.getLogger(__name__)


def include_routers(dp: Dispatcher):
    """Регистрация хендлеров"""
    dp.include_routers()


def include_filters(dp: Dispatcher):
    """Регистрация фильтров для хендлеров"""
    dp.message.filter(F.chat.type == "private")
    dp.callback_query.filter(F.chat.type == "private")


async def main():
    bot = Bot(token="", parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    include_filters(dp)

    include_routers(dp)

    await set_commands(bot, settings.ADMINS)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await dp.stop_polling()


if __name__ == "__main__":
    try:
        logger.info("Bot starting...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopping...")
