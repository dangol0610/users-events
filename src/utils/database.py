from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.settings.settings import settings


class Database:
    """Управление подключением к БД"""

    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    async def init(self):
        """Инициализация пула подключений"""
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.DEBUG,  # ← Логировать только в dev
            pool_size=settings.DB_POOL_SIZE,  # ← 20
            max_overflow=settings.DB_MAX_OVERFLOW,  # ← 40
            pool_pre_ping=settings.DB_POOL_PRE_PING,  # ← True
            pool_recycle=settings.DB_POOL_RECYCLE,  # ← 3600
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        logger.info(
            f"Database initialized "
            f"(pool_size={settings.DB_POOL_SIZE}, "
            f"max_overflow={settings.DB_MAX_OVERFLOW})"
        )

    async def close(self):
        """Закрытие пула подключений"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Генератор сессий для Depends()"""
        if self.session_factory is None:
            raise RuntimeError("Database not initialized. Call init() first.")

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


# Database instance
db = Database()


# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass
