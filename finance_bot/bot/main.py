"""Bot entry point."""
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config.logging_config import setup_logging
from bot.config.settings import settings
from bot.database.db_provider import init_db
from bot.handlers import callbacks, common, finances, start, wishlist
from bot.utils.logging import get_logger

logger = get_logger(__name__)


def register_routers(dispatcher: Dispatcher) -> None:
    """Register all routers."""
    dispatcher.include_router(start.router)
    dispatcher.include_router(common.router)
    dispatcher.include_router(finances.router)
    dispatcher.include_router(wishlist.router)
    dispatcher.include_router(callbacks.router)


async def main() -> None:
    """Run the bot."""
    setup_logging()
    if not settings.bot_token:
        logger.error("BOT_TOKEN is not set. Please configure .env file.")
        return

    await init_db()
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    register_routers(dp)

    logger.info("Starting bot polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
