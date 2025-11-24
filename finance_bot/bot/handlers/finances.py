"""Finance handlers."""
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database import crud
from bot.database.db_provider import get_session
from bot.database.models import OperationType
from bot.keyboards.main import MAIN_MENU
from bot.states.money_states import MoneyStates

router = Router()

FINANCE_OPTIONS = {
    "доход": OperationType.INCOME,
    "расход": OperationType.EXPENSE,
    "спонтанная трата": OperationType.SPONTANEOUS,
}


@router.message(Command("finance"))
@router.message(F.text == "💰 Финансы")
async def finance_entry(message: Message, state: FSMContext) -> None:
    """Entry point to finance flow."""
    await state.set_state(MoneyStates.choosing_type)
    options = "\n".join(["- Доход", "- Расход", "- Спонтанная трата"])
    await message.answer(f"Выберите тип операции:\n{options}")


@router.message(MoneyStates.choosing_type)
async def choose_type(message: Message, state: FSMContext) -> None:
    """Handle operation type selection."""
    text = message.text.lower()
    op_type = FINANCE_OPTIONS.get(text)
    if not op_type:
        await message.answer("Пожалуйста, выберите: доход, расход или спонтанная трата.")
        return
    await state.update_data(op_type=op_type)
    await state.set_state(MoneyStates.choosing_category)
    await message.answer("Укажите категорию операции (например, еда, зарплата, развлечения).")


@router.message(MoneyStates.choosing_category)
async def set_category(message: Message, state: FSMContext) -> None:
    """Handle category input."""
    await state.update_data(category=message.text)
    await state.set_state(MoneyStates.entering_amount)
    await message.answer("Введите сумму операции (число).")


@router.message(MoneyStates.entering_amount)
async def set_amount(message: Message, state: FSMContext) -> None:
    """Handle amount input."""
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Сумма должна быть числом. Попробуйте снова.")
        return
    await state.update_data(amount=amount)
    await state.set_state(MoneyStates.entering_comment)
    await message.answer("Добавьте комментарий или отправьте '-' чтобы пропустить.")


@router.message(MoneyStates.entering_comment)
async def set_comment(message: Message, state: FSMContext) -> None:
    """Handle comment input."""
    comment = None if message.text.strip() == "-" else message.text
    await state.update_data(comment=comment)
    data = await state.get_data()
    op_type = data.get("op_type")
    category = data.get("category")
    amount = data.get("amount")
    comment = data.get("comment")
    await state.set_state(MoneyStates.confirming)
    await message.answer(
        f"Подтвердите операцию:\nТип: {op_type.value}\nКатегория: {category}\nСумма: {amount}\nКомментарий: {comment or '—'}\nОтправьте 'да' для подтверждения или /cancel для отмены."
    )


@router.message(MoneyStates.confirming)
async def confirm_operation(message: Message, state: FSMContext) -> None:
    """Persist operation after confirmation."""
    if message.text.lower() not in {"да", "yes", "ок"}:
        await message.answer("Операция не сохранена. Используйте /cancel для отмены или введите 'да' для сохранения.")
        return
    data = await state.get_data()
    telegram_id = message.from_user.id
    async for session in get_session():
        user = await crud.create_user_if_not_exists(session, telegram_id)
        await crud.add_operation(
            session,
            user=user,
            op_type=data["op_type"],
            category=data["category"],
            amount=data["amount"],
            comment=data.get("comment"),
        )
    await message.answer("Операция сохранена!", reply_markup=MAIN_MENU)
    await state.clear()


@router.message(F.text == "📊 Статистика")
@router.message(Command("stats"))
async def show_stats(message: Message) -> None:
    """Show basic statistics."""
    telegram_id = message.from_user.id
    async for session in get_session():
        user = await crud.create_user_if_not_exists(session, telegram_id)
        stats = await crud.get_statistics(session, user, period="week")
    text = (
        "Статистика за неделю:\n"
        f"Расходы: {stats['expenses']}\n"
        f"Доходы: {stats['incomes']}\n"
        f"Спонтанные траты: {stats['spontaneous']}\n"
        f"Выполненных желаний: {stats['wishlist_done']}"
    )
    await message.answer(text)
