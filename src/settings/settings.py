import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения
    """

    # Database settings
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="postgres")
    POSTGRES_HOST: str = Field(default="postgres")
    POSTGRES_PORT: int = Field(default=5432)

    # Database pool settings
    DB_POOL_SIZE: int = Field(default=20)
    DB_MAX_OVERFLOW: int = Field(default=40)
    DB_POOL_RECYCLE: int = Field(default=3600)
    DB_POOL_PRE_PING: bool = Field(default=True)
    DEBUG: bool = Field(default=False)

    # Redis settings
    REDIS_HOST: str = Field(default="redis")
    REDIS_PORT: int = Field(default=6379)
    REDIS_CACHE_DB: int = Field(default=0)
    REDIS_BROKER_DB: int = Field(default=1)
    REDIS_RESULT_DB: int = Field(default=2)
    CACHE_TTL: int = Field(default=3600)
    REDIS_MAX_CONNECTIONS: int = Field(default=50)

    # RabbitMQ settings
    RABBITMQ_HOST: str = Field(default="localhost")
    RABBITMQ_PORT: int = Field(default=5672)
    RABBITMQ_USER: str = Field(default="guest")
    RABBITMQ_PASSWORD: str = Field(default="guest")

    # JWT settings
    SECRET_KEY: str = Field(default="")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRES_MINUTES: int = Field(default=15)
    REFRESH_TOKEN_EXPIRES_DAYS: int = Field(default=7)

    @property
    def database_url(self) -> str:
        """URL для подключения к базе данных"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def redis_url(self) -> str:
        """URL для подключения к Redis"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_CACHE_DB}"

    @property
    def redis_broker_url(self) -> str:
        """URL для подключения к Redis брокеру"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_BROKER_DB}"

    @property
    def redis_result_url(self) -> str:
        """URL для подключения к Redis для результатов"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_RESULT_DB}"

    @property
    def rabbitmq_url(self) -> str:
        """URL для подключения к RabbitMQ"""
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    model_config = SettingsConfigDict(
        env_file="src/.env.test" if os.getenv("TESTING") == "True" else "src/.env"
    )


settings = Settings()
