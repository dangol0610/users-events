from faststream.rabbit import RabbitRouter
from loguru import logger

from src.broker.schemas import EVENT_CREATED_QUEUE, EventCreatedMessage

events_consumer_router = RabbitRouter()


@events_consumer_router.subscriber(EVENT_CREATED_QUEUE)
async def handle_event_created(msg: EventCreatedMessage):
    logger.info(f"Received event created: {msg}")
