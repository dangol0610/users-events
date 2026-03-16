from loguru import logger
from redis.asyncio import ConnectionPool, Redis

from src.settings.settings import settings


class RedisManager:
    """
    Управляет подключением к Redis.
    """

    def __init__(self):
        self.pool: ConnectionPool | None = None
        self.redis: Redis | None = None

    async def init(self) -> None:
        self.pool = ConnectionPool.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )
        self.redis = Redis(connection_pool=self.pool)
        logger.info("Redis initialized")

    async def close(self) -> None:
        """
        Закрывает подключение к Redis.
        """
        if self.redis:
            await self.redis.close()
            logger.info("Redis closed")

    def get_redis(self) -> Redis:
        """
        Возвращает экземпляр Redis.
        """
        if not self.redis:
            raise RuntimeError("Redis not initialized")
        return self.redis


# Redis manager instance
redis_manager = RedisManager()
