"""Callback query handlers."""
from aiogram import Router
from aiogram.types import CallbackQuery

from bot.database import crud
from bot.database.db_provider import get_session

router = Router()


@router.callback_query()
async def handle_callback(callback: CallbackQuery) -> None:
    """Generic callback handler for marking wishlist items done.

    Expects data in format ``done:<id>``.
    """
    data = callback.data or ""
    if not data.startswith("done:"):
        await callback.answer()
        return
    _, item_id_str = data.split(":", maxsplit=1)
    if not item_id_str.isdigit():
        await callback.answer("Некорректный идентификатор")
        return
    telegram_id = callback.from_user.id
    async for session in get_session():
        user = await crud.create_user_if_not_exists(session, telegram_id)
        updated = await crud.mark_wishlist_item_done(session, int(item_id_str), user)
    if not updated:
        await callback.answer("Не удалось найти элемент")
        return
    await callback.answer("Готово!", show_alert=False)
