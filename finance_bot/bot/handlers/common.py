"""Common handlers."""
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.main import MAIN_MENU

router = Router()


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext) -> None:
    """Cancel current state."""
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=MAIN_MENU)
