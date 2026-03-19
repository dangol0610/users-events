from loguru import logger
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.apps.events.models import Event
from src.apps.events.schemas import CreateEventDTO


class EventRepository:
    """Репозиторий для операций с событиями в базе данных."""

    def __init__(self, session):
        """Инициализация репозитория с сессией базы данных."""
        self.session = session

    async def create_event(self, event_data: CreateEventDTO, user_id: int) -> Event:
        """Создание нового события в базе данных."""
        try:
            event_to_insert = event_data.model_dump()
            event_to_insert["user_id"] = user_id
            stmt = insert(Event).values(event_to_insert).returning(Event)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError:
            logger.exception("Failed to create event")
            raise

    async def get_event_by_user(self, user_id: int) -> list[Event]:
        """Получение всех событий пользователя."""
        try:
            query = select(Event).where(Event.user_id == user_id)
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError:
            logger.exception(f"Failed to get event by user {user_id}")
            raise
