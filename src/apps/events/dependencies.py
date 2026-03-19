from typing import Annotated

from fastapi import Depends

from src.apps.events.repoository import EventRepository
from src.apps.events.services import EventService
from src.utils.dependencies import BrokerDependency, RedisDependency, SessionDependency


def get_event_repository(session: SessionDependency) -> EventRepository:
    return EventRepository(session)


EventRepositoryDependency = Annotated[EventRepository, Depends(get_event_repository)]


def get_event_service(
    event_repo: EventRepositoryDependency,
    redis: RedisDependency,
    broker: BrokerDependency,
) -> EventService:
    return EventService(repository=event_repo, redis=redis, broker=broker)


EventServiceDependency = Annotated[EventService, Depends(get_event_service)]
