from datetime import datetime

from pydantic import BaseModel


class EventCreatedMessage(BaseModel):
    """
    Сообщение о создании события для публикации в RabbitMQ.

    Используется для уведомления других сервисов о создании нового события.
    """

    event_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


"""Название очереди для сообщений о создании событий"""
EVENT_CREATED_QUEUE = "events.created"
