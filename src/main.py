from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.broker.serve import app as broker_app
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
    await broker_app.start()
    logger.info("DB, Redis, Broker initialized")

    yield

    await db.close()
    await redis_manager.close()
    await broker_app.stop()
    logger.info("DB, Redis, Broker closed")


app = FastAPI(
    title="Users Service",
    description="Сервис создания и получения пользователей",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)
