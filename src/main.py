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
    Контекстный менеджер для инициализации и закрытия соединений с базой данных, Redis и брокером FastStream для отправки.
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


"""Приложение FastAPI для сервиса пользователей с авторизацией и управлением событиями."""
app = FastAPI(
    title="Users Service",
    description="Сервис пользователей с авторизацией и управлением событиями",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)
