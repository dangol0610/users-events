from fastapi import APIRouter, HTTPException, status

from src.apps.auth.dependencies import CurrentUserDependency
from src.apps.users.dependencies import UserServiceDependency
from src.apps.users.schemas import ReturnUserDTO, UpdateUserDTO
from src.utils.exceptions import CacheError, DatabaseError, NotFoundError

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/me")
async def get_me(user: CurrentUserDependency) -> ReturnUserDTO:
    """Return the current user's profile."""
    return user


@users_router.patch("/me")
async def update_me(
    user: CurrentUserDependency,
    update_data: UpdateUserDTO,
    user_service: UserServiceDependency,
) -> ReturnUserDTO:
    """Update the current user's profile."""
    try:
        updated = await user_service.update_user(
            user_id=user.id,
            user_data=update_data,
        )
        return updated
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}",
        )
    except (CacheError, DatabaseError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@users_router.delete("/me")
async def delete_me(
    user: CurrentUserDependency,
    user_service: UserServiceDependency,
) -> ReturnUserDTO:
    """Delete the current user's profile."""
    try:
        deleted = await user_service.delete_user(user_id=user.id)
        return deleted
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}",
        )
    except (CacheError, DatabaseError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )
