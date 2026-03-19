from typing import Annotated

from fastapi import Depends

from src.apps.users.repository import UserRepository
from src.apps.users.services import UserService
from src.utils.dependencies import RedisDependency, SessionDependency

"""Модуль зависимостей для пользователей."""


def get_user_repo(session: SessionDependency) -> UserRepository:
    """Функция для получения репозитория пользователей."""
    return UserRepository(session)


"""Аннотация зависимости для репозитория пользователей."""
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repo)]


def get_user_service(
    user_repo: UserRepositoryDependency, redis: RedisDependency
) -> UserService:
    """Функция зависимости для сервиса пользователей."""
    return UserService(user_repo, redis)


"""Аннотация зависимости для сервиса пользователей."""
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
