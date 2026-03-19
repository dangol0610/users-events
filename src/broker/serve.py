from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.settings.settings import settings

broker = RabbitBroker(url=settings.rabbitmq_url)
app = FastStream(broker)
