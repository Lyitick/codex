"""Wishlist handlers."""
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database import crud
from bot.database.db_provider import get_session
from bot.keyboards.main import MAIN_MENU
from bot.states.wishlist_states import WishlistStates

router = Router()


@router.message(Command("wishlist"))
@router.message(F.text == "🎯 Вишлист")
async def wishlist_entry(message: Message, state: FSMContext) -> None:
    """Entry point for wishlist flow."""
    await state.set_state(WishlistStates.entering_title)
    await message.answer("Введите название желания.")


@router.message(WishlistStates.entering_title)
async def set_title(message: Message, state: FSMContext) -> None:
    """Handle wishlist title input."""
    await state.update_data(title=message.text)
    await state.set_state(WishlistStates.entering_amount)
    await message.answer("Укажите ориентировочную сумму.")


@router.message(WishlistStates.entering_amount)
async def set_amount(message: Message, state: FSMContext) -> None:
    """Handle wishlist amount input."""
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Сумма должна быть числом. Попробуйте снова.")
        return
    await state.update_data(amount=amount)
    await state.set_state(WishlistStates.entering_priority)
    await message.answer("Выберите приоритет (1-5, где 1 — высокий).")


@router.message(WishlistStates.entering_priority)
async def set_priority(message: Message, state: FSMContext) -> None:
    """Handle priority input."""
    try:
        priority = int(message.text)
    except ValueError:
        await message.answer("Приоритет должен быть числом от 1 до 5.")
        return
    if priority < 1 or priority > 5:
        await message.answer("Приоритет должен быть в диапазоне 1-5.")
        return
    await state.update_data(priority=priority)
    data = await state.get_data()
    await state.set_state(WishlistStates.confirming)
    await message.answer(
        f"Подтвердите желание:\nНазвание: {data['title']}\nСумма: {data['amount']}\nПриоритет: {priority}\nОтправьте 'да' для сохранения или /cancel для отмены."
    )


@router.message(WishlistStates.confirming)
async def confirm_wishlist(message: Message, state: FSMContext) -> None:
    """Persist wishlist item."""
    if message.text.lower() not in {"да", "yes", "ок"}:
        await message.answer("Желание не сохранено. Используйте /cancel или отправьте 'да' для сохранения.")
        return
    data = await state.get_data()
    telegram_id = message.from_user.id
    async for session in get_session():
        user = await crud.create_user_if_not_exists(session, telegram_id)
        await crud.add_wishlist_item(
            session,
            user=user,
            title=data["title"],
            target_amount=data["amount"],
            priority=data["priority"],
        )
    await message.answer("Желание сохранено!", reply_markup=MAIN_MENU)
    await state.clear()


@router.message(Command("list"))
async def list_wishlist(message: Message) -> None:
    """List wishlist items."""
    telegram_id = message.from_user.id
    async for session in get_session():
        user = await crud.create_user_if_not_exists(session, telegram_id)
        items = await crud.list_wishlist_items(session, user)
    if not items:
        await message.answer("Ваш список желаний пуст.")
        return
    lines = []
    for item in items:
        status = "✅" if item.is_done else "⌛"
        lines.append(f"{status} {item.title} — {item.target_amount} (приоритет {item.priority})")
    await message.answer("\n".join(lines))
