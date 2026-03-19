from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.apps.consumers.events.handlers import events_consumer_router
from src.settings.settings import settings

consumer_broker = RabbitBroker(url=settings.rabbitmq_url, reconnect_interval=5)
consumer_fs_app = FastStream(consumer_broker)

consumer_broker.include_router(events_consumer_router)
