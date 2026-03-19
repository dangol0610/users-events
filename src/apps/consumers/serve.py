"""
Модуль настройки и запуска FastStream consumer.

Этот модуль инициализирует брокер RabbitMQ и регистрирует обработчики сообщений.
Запускается как отдельный процесс через `faststream run`.
"""

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.apps.consumers.events.handlers import events_consumer_router
from src.settings.settings import settings

"""
Брокер для потребления сообщений из RabbitMQ.

Параметры:
    url: URL подключения к RabbitMQ из настроек
    reconnect_interval: Интервал переподключения при потере связи (5 секунд)
"""
consumer_broker = RabbitBroker(url=settings.rabbitmq_url, reconnect_interval=5)

"""FastStream приложение для consumer"""
consumer_fs_app = FastStream(consumer_broker)

"""Регистрация роутера с обработчиками сообщений"""
consumer_broker.include_router(events_consumer_router)
