from fastapi import APIRouter

from src.apps.auth.dependencies import CurrentUserDependency
from src.apps.users.schemas import ReturnUserDTO

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/me")
async def get_me(user: CurrentUserDependency) -> ReturnUserDTO:
    """Return the current user's profile."""
    return ReturnUserDTO.model_validate(user)
