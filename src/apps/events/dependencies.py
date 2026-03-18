from typing import Annotated

from fastapi import Depends

from src.apps.events.repoository import EventRepository
from src.apps.events.services import EventService
from src.utils.dependencies import RedisDependency, SessionDependency


def get_event_repository(session: SessionDependency) -> EventRepository:
    return EventRepository(session)


EventRepositoryDependency = Annotated[EventRepository, Depends(get_event_repository)]


def get_event_service(
    event_repo: EventRepositoryDependency, redis: RedisDependency
) -> EventService:
    return EventService(event_repo, redis)


EventServiceDependency = Annotated[EventService, Depends(get_event_service)]
