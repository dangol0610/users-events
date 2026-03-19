"""
Обработчики сообщений для событий.

Этот модуль содержит обработчики сообщений из RabbitMQ очереди событий.
"""

from faststream.rabbit import RabbitRouter
from loguru import logger

from src.broker.schemas import EVENT_CREATED_QUEUE, EventCreatedMessage

"""Роутер для обработки сообщений из очереди событий"""
events_consumer_router = RabbitRouter()


@events_consumer_router.subscriber(EVENT_CREATED_QUEUE)
async def handle_event_created(msg: EventCreatedMessage) -> None:
    """
    Обработчик сообщения о создании события.
    Получает сообщение из очереди `events.created` и логирует информацию о событии.
    """
    logger.info(f"Received event created: {msg}")
