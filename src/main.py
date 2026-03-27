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
    Context manager for initializing and closing connections to database, Redis, and FastStream broker.

    Handles startup and shutdown of all external services including database connection pool,
    Redis connection, and message broker.
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


"""FastAPI application for user service with authentication and event management."""
app = FastAPI(
    title="Users Service",
    description="User service with authentication and event management",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)


nums = [3, 0, 1]
res = [i for i in range(len(nums)) if i not in nums]
print(res)
