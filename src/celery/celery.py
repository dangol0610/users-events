from celery.signals import worker_init
from loguru import logger

from celery import Celery
from src.settings.settings import settings


def create_celery_app() -> Celery:
    """Создание и  конфигурация Celery приложения."""
    app = Celery(
        "users_events",
        broker=settings.redis_broker_url,
        backend=settings.redis_result_url,
        include=["src.celery.tasks"],
    )

    app.conf.update(
        # Сериализация
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        # Retry
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        task_default_retry_delay=10,
        task_max_retries=3,
        # Таймауты
        task_time_limit=300,
        task_soft_time_limit=240,
        # Rate limiting
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=1000,
    )

    return app


@worker_init.connect
def on_worker_init(sender=None, **kwargs):
    """Сигнал, отправляемый при инициализации воркера Celery."""
    logger.info("Worker initialized")


"""Экземпляр Celery приложения."""
celery_app = create_celery_app()
