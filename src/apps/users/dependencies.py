from typing import Annotated

from fastapi import Depends

from src.apps.users.repository import UserRepository
from src.apps.users.services import UserService
from src.utils.dependencies import RedisDependency, SessionDependency


def get_user_repo(session: SessionDependency) -> UserRepository:
    return UserRepository(session)


UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repo)]


def get_user_service(
    user_repo: UserRepositoryDependency, redis: RedisDependency
) -> UserService:
    return UserService(user_repo, redis)


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
