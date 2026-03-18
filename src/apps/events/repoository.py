from loguru import logger
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.apps.events.models import Event
from src.apps.events.schemas import CreateEventDTO


class EventRepository:
    """Repository for event-related database operations"""

    def __init__(self, session):
        self.session = session

    async def create_event(self, event_data: CreateEventDTO, user_id: int) -> Event:
        try:
            event_to_insert = event_data.model_dump()
            event_to_insert["user_id"] = user_id
            stmt = insert(Event).values(event_to_insert).returning(Event)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except SQLAlchemyError:
            logger.error("Failed to create event")
            raise

    async def get_event_by_id(self, event_id: int):
        try:
            query = select(Event).where(Event.id == event_id)
            result = await self.session.execute(query)
            await self.session.commit()
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            logger.exception(f"Failed to get event by id {event_id}")
            raise
