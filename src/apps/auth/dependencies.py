from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger

from src.apps.auth.services import AuthService
from src.apps.users.dependencies import UserRepositoryDependency, UserServiceDependency
from src.apps.users.schemas import ReturnUserDTO
from src.settings.settings import settings
from src.utils.dependencies import RedisDependency
from src.utils.token_utils import TokenUtils

security = HTTPBearer()


async def get_current_user(
    user_repo: UserRepositoryDependency,
    redis: RedisDependency,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ReturnUserDTO:
    """Get the current authenticated user from JWT token."""
    if not credentials:
        logger.error("No credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No credentials provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    try:
        payload = TokenUtils.decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            logger.error("Invalid token: missing user ID")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        cached_user = await redis.get(f"user:{user_id}")
        if cached_user:
            logger.info(f"User {user_id} found in cache")
            user_dto = ReturnUserDTO.model_validate_json(cached_user)
            return user_dto

        user = await user_repo.get_user_by_id(int(user_id))
        if not user:
            logger.error("Invalid token: user not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_dto = ReturnUserDTO.model_validate(user)
        await redis.set(
            f"user:{user_id}", user_dto.model_dump_json(), ex=settings.CACHE_TTL
        )
        logger.info(f"User {user_id} cached")
        return user_dto
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_auth_service(user_service: UserServiceDependency) -> AuthService:
    return AuthService(user_service)


CurrentUserDependency = Annotated[ReturnUserDTO, Depends(get_current_user)]
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
