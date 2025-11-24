"""Database session provider."""
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.config.settings import settings
from bot.database.models import Base
from bot.utils.logging import get_logger

logger = get_logger(__name__)

engine = create_async_engine(settings.database_url, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    """Initialize database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")


async def get_session() -> AsyncIterator[AsyncSession]:
    """Provide an async database session.

    Yields:
        AsyncSession: Active database session.
    """
    async with SessionLocal() as session:
        yield session
