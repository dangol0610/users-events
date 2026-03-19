from typing import Annotated

from fastapi import Depends
from faststream.rabbit import RabbitBroker
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.broker.serve import broker
from src.utils.database import db
from src.utils.redis import redis_manager


def get_broker() -> RabbitBroker:
    """Функция зависимости для получения брокера RabbitMQ."""
    return broker


"""Зависимость для получения брокера RabbitMQ."""
BrokerDependency = Annotated[RabbitBroker, Depends(get_broker)]
"""Зависимость для получения сессии базы данных."""
SessionDependency = Annotated[AsyncSession, Depends(db.get_session)]
"""Зависимость для получения клиента Redis."""
RedisDependency = Annotated[Redis, Depends(redis_manager.get_redis)]
