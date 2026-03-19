from typing import Annotated

from fastapi import Depends

from src.apps.events.repository import EventRepository
from src.apps.events.services import EventService
from src.utils.dependencies import BrokerDependency, RedisDependency, SessionDependency

"""
Модуль зависимостей для приложения events.

Содержит функции для получения зависимостей:
- EventRepositoryDependency: репозиторий событий
- EventServiceDependency: сервис событий
"""


def get_event_repository(session: SessionDependency) -> EventRepository:
    """Функция зависимости для EventRepository."""
    return EventRepository(session)


"""Аннотация зависимости для EventRepository."""
EventRepositoryDependency = Annotated[EventRepository, Depends(get_event_repository)]


def get_event_service(
    event_repo: EventRepositoryDependency,
    redis: RedisDependency,
    broker: BrokerDependency,
) -> EventService:
    """Функция зависимости для EventService."""
    return EventService(repository=event_repo, redis=redis, broker=broker)


"""Аннотация зависимости для EventService."""
EventServiceDependency = Annotated[EventService, Depends(get_event_service)]
