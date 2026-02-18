from typing import AsyncGenerator
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True,
    future=True,
)


async def init_db():
    """Initialize database tables"""
    from app.models.user import User

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async_session = AsyncSession(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session:
        yield async_session


# Sync engine for compatibility
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)


def get_db():
    """Get sync database session (for compatibility)"""
    with Session(sync_engine) as session:
        yield session
