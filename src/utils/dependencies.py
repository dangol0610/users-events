from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import db
from src.utils.redis import redis_manager

SessionDependency = Annotated[AsyncSession, Depends(db.get_session)]
RedisDependency = Annotated[Redis, Depends(redis_manager.get_redis)]
