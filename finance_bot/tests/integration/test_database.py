"""Integration tests for database CRUD operations."""
import pytest
import pytest_asyncio

from bot.database import crud
from bot.database.db_provider import get_session, engine
from bot.database.models import Base, OperationType


@pytest_asyncio.fixture(autouse=True, scope="module")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user_and_operation() -> None:
    async for session in get_session():
        user = await crud.create_user_if_not_exists(session, telegram_id=123)
        op = await crud.add_operation(session, user, OperationType.INCOME, "зарплата", 1000.0)
        assert op.id is not None
        operations = await crud.get_operations_for_period(session, user, "day")
        assert len(operations) == 1


@pytest.mark.asyncio
async def test_wishlist_crud() -> None:
    async for session in get_session():
        user = await crud.create_user_if_not_exists(session, telegram_id=456)
        item = await crud.add_wishlist_item(session, user, "Телефон", 50000, 2)
        items = await crud.list_wishlist_items(session, user)
        assert len(items) == 1
        updated = await crud.mark_wishlist_item_done(session, item.id, user)
        assert updated is not None
        assert updated.is_done is True
