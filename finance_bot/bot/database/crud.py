"""CRUD operations."""
from datetime import datetime, timedelta
from typing import Iterable, Sequence

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Operation, OperationType, User, WishlistItem


async def create_user_if_not_exists(session: AsyncSession, telegram_id: int) -> User:
    """Create a user if not exists.

    Args:
        session: Database session.
        telegram_id: Telegram user id.

    Returns:
        User: Existing or newly created user.
    """
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        return user
    user = User(telegram_id=telegram_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def add_operation(
    session: AsyncSession,
    user: User,
    op_type: OperationType,
    category: str,
    amount: float,
    comment: str | None = None,
) -> Operation:
    """Add a financial operation."""
    operation = Operation(user_id=user.id, type=op_type, category=category, amount=amount, comment=comment)
    session.add(operation)
    await session.commit()
    await session.refresh(operation)
    return operation


async def get_operations_for_period(
    session: AsyncSession, user: User, period: str = "day"
) -> Sequence[Operation]:
    """Get operations for a given period.

    Args:
        session: Database session.
        user: User owner.
        period: Period string (day, week, month).

    Returns:
        Sequence[Operation]: List of operations.
    """
    now = datetime.utcnow()
    start_map = {
        "day": now - timedelta(days=1),
        "week": now - timedelta(weeks=1),
        "month": now - timedelta(days=30),
    }
    start_date = start_map.get(period, start_map["day"])
    result = await session.execute(
        select(Operation).where(and_(Operation.user_id == user.id, Operation.created_at >= start_date)).order_by(Operation.created_at)
    )
    return result.scalars().all()


async def add_wishlist_item(
    session: AsyncSession, user: User, title: str, target_amount: float, priority: int
) -> WishlistItem:
    """Add a wishlist item."""
    item = WishlistItem(user_id=user.id, title=title, target_amount=target_amount, priority=priority)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def list_wishlist_items(session: AsyncSession, user: User) -> Iterable[WishlistItem]:
    """List wishlist items for a user."""
    result = await session.execute(select(WishlistItem).where(WishlistItem.user_id == user.id).order_by(WishlistItem.created_at))
    return result.scalars().all()


async def mark_wishlist_item_done(session: AsyncSession, item_id: int, user: User) -> WishlistItem | None:
    """Mark wishlist item as done."""
    result = await session.execute(
        select(WishlistItem).where(and_(WishlistItem.id == item_id, WishlistItem.user_id == user.id))
    )
    item = result.scalar_one_or_none()
    if not item:
        return None
    item.is_done = True
    item.done_at = datetime.utcnow()
    await session.commit()
    await session.refresh(item)
    return item


async def get_statistics(session: AsyncSession, user: User, period: str = "week") -> dict[str, float | int]:
    """Get basic statistics."""
    operations = await get_operations_for_period(session, user, period)
    expenses = sum(op.amount for op in operations if op.type == OperationType.EXPENSE)
    incomes = sum(op.amount for op in operations if op.type == OperationType.INCOME)
    spontaneous = sum(op.amount for op in operations if op.type == OperationType.SPONTANEOUS)

    wishlist_result = await session.execute(select(func.count(WishlistItem.id)).where(and_(WishlistItem.user_id == user.id, WishlistItem.is_done)))
    wishlist_done = wishlist_result.scalar_one()

    return {
        "expenses": expenses,
        "incomes": incomes,
        "spontaneous": spontaneous,
        "wishlist_done": wishlist_done,
    }
