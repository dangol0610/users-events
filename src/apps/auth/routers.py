from fastapi import APIRouter, HTTPException, status

from src.apps.auth.dependencies import AuthServiceDependency
from src.apps.auth.schemas import (
    RefreshTokenSchema,
    TokenSchema,
    UserLoginSchema,
    UserRegisterSchema,
)
from src.apps.users.schemas import ReturnUserDTO
from src.utils.exceptions import (
    AuthenticationError,
    DatabaseError,
    InvalidTokenError,
    NotFoundError,
    UserAlreadyExistsError,
)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def register(
    user: UserRegisterSchema,
    auth_service: AuthServiceDependency,
) -> ReturnUserDTO:
    """Register a new user. Returns a ReturnUserDTO on success. Raises HTTPException on failure."""
    try:
        return await auth_service.register(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{e}",
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@auth_router.post("/login")
async def login(
    user: UserLoginSchema,
    auth_service: AuthServiceDependency,
) -> TokenSchema:
    """Login a user. Returns a TokenSchema on success. Raises HTTPException on failure."""
    try:
        return await auth_service.login(user)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}",
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}",
        )


@auth_router.post("/refresh")
async def refresh(
    token: RefreshTokenSchema, auth_service: AuthServiceDependency
) -> TokenSchema:
    """Refresh a token. Returns a TokenSchema on success. Raises HTTPException on failure."""
    try:
        return await auth_service.refresh_token(token.token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}",
        )
