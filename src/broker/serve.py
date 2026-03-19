from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.settings.settings import settings

"""Сервер брокера RabbitMQ для публикации."""
broker = RabbitBroker(url=settings.rabbitmq_url)
"""Приложение FastStream для публикации событий."""
app = FastStream(broker)
