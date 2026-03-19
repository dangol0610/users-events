"""
Сервис для управления событиями.

Этот модуль содержит бизнес-логику для создания и получения событий.
Включает кэширование в Redis и публикацию событий в RabbitMQ.
"""

import json

from faststream.exceptions import FastStreamException
from faststream.rabbit import RabbitBroker
from loguru import logger
from redis.asyncio import Redis, RedisError
from sqlalchemy.exc import SQLAlchemyError

from src.apps.events.repository import EventRepository
from src.apps.events.schemas import CreateEventDTO, ReturnEventDTO
from src.broker.schemas import EVENT_CREATED_QUEUE, EventCreatedMessage
from src.utils.exceptions import CacheError, DatabaseError, FastStreamError


class EventService:
    """
    Сервис для работы с событиями.

    Отвечает за создание и получение событий пользователя с кэшированием
    и публикацией событий в очередь сообщений (RabbitMQ).

    Attributes:
        repository: Репозиторий для операций с базой данных
        broker: Брокер для публикации сообщений в RabbitMQ
        redis: Redis клиент для кэширования
        cache_ttl: Время жизни кэша в секундах (по умолчанию 60)
    """

    def __init__(self, repository: EventRepository, redis: Redis, broker: RabbitBroker):
        self.repository = repository
        self.broker = broker
        self.redis = redis
        self.cache_ttl = 60

    async def create_event(
        self, event_data: CreateEventDTO, user_id: int
    ) -> ReturnEventDTO:
        """
        Создать новое событие.

        Создаёт событие в базе данных и публикует сообщение в RabbitMQ очередь
        для уведомления других сервисов.

        Args:
            event_data: Данные для создания события (title, description)
            user_id: ID пользователя, создающего событие

        Returns:
            ReturnEventDTO: Данные созданного события

        Raises:
            DatabaseError: При ошибке базы данных
            FastStreamError: При ошибке публикации в брокер
        """
        try:
            event = await self.repository.create_event(event_data, user_id)
            logger.info(f"Event created: {event.id}")

            await self.broker.publish(
                message=EventCreatedMessage(
                    event_id=event.id,
                    user_id=user_id,
                    created_at=event.created_at,
                    updated_at=event.updated_at,
                ),
                queue=EVENT_CREATED_QUEUE,
            )
            logger.info(
                f"Event created message published to queue: {EVENT_CREATED_QUEUE}"
            )

            return ReturnEventDTO.model_validate(event)
        except SQLAlchemyError:
            logger.exception("SQL Alchemy error while creating event")
            raise DatabaseError("Failed to create event")
        except FastStreamException:
            logger.exception("FastStream error while publishing event created message")
            raise FastStreamError("Failed to publish event created message")

    async def get_event_by_user(self, user_id: int) -> list[ReturnEventDTO]:
        """
        Получить список событий пользователя.

        Сначала проверяет кэш в Redis, при отсутствии — загружает из базы данных
        и кэширует результат.

        Args:
            user_id: ID пользователя, чьи события нужно получить

        Returns:
            list[ReturnEventDTO]: Список событий пользователя

        Raises:
            DatabaseError: При ошибке базы данных
            CacheError: При ошибке Redis
        """
        try:
            cached = await self.redis.get(f"user:{user_id}:events")
            if cached:
                logger.info(f"Events found for user {user_id} in cache")
                return [
                    ReturnEventDTO.model_validate(event) for event in json.loads(cached)
                ]

            events = await self.repository.get_event_by_user(user_id)
            events_return = [ReturnEventDTO.model_validate(event) for event in events]
            events_json = json.dumps(
                [event.model_dump(mode="json") for event in events_return]
            )
            logger.info(f"Events found for user {user_id}: {len(events)}")

            await self.redis.set(
                f"user:{user_id}:events", events_json, ex=self.cache_ttl
            )
            logger.info(f"Events cached for user {user_id}")

            return events_return
        except SQLAlchemyError:
            logger.exception(
                f"SQL Alchemy error while getting events for user {user_id}"
            )
            raise DatabaseError("Failed to get events for user")
        except RedisError:
            logger.exception(f"Redis error while getting events for user {user_id}")
            raise CacheError("Failed to get events for user")
