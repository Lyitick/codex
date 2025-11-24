"""Start command handler."""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database import crud
from bot.keyboards.main import MAIN_MENU
from bot.utils.logging import get_logger
from bot.database.db_provider import get_session

router = Router()
logger = get_logger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start command."""
    telegram_id = message.from_user.id
    async for session in get_session():
        await crud.create_user_if_not_exists(session, telegram_id)
    greeting = (
        "Привет! Я помогу вести учёт финансов и желаний.\n"
        "Доступно: добавление доходов и расходов, спонтанные траты, вишлист и статистика."
    )
    await message.answer(greeting, reply_markup=MAIN_MENU)
    logger.info("User %s started bot", telegram_id)
