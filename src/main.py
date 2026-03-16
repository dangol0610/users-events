from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.routers.api_router import router as api_router
from src.utils.database import db
from src.utils.redis import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Закрытие соединений с базой данных и Redis
    """
    await db.init()
    await redis_manager.init()
    logger.info("DB and Redis initialized")

    yield

    await db.close()
    await redis_manager.close()
    logger.info("DB and Redis closed")


app = FastAPI(
    title="Users Service",
    description="Сервис создания и получения пользователей",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)
