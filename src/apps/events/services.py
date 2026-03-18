from loguru import logger
from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError

from src.apps.events.repoository import EventRepository
from src.apps.events.schemas import CreateEventDTO, ReturnEventDTO
from src.utils.exceptions import DatabaseError


class EventService:
    def __init__(self, repository: EventRepository, redis: Redis):
        self.repository = repository
        self.redis = redis
        self.cache_ttl = 60

    async def create_event(
        self, event_data: CreateEventDTO, user_id: int
    ) -> ReturnEventDTO:
        try:
            event = await self.repository.create_event(event_data, user_id)
            logger.info(f"Event created: {event.id}")
            return ReturnEventDTO.model_validate(event)
        except SQLAlchemyError:
            logger.exception("SQL Alchemy error while creating event")
            raise DatabaseError("Failed to create event")
