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
    """
    Register a new user.
    
    Args:
        user: User registration data (email, username, password)
        auth_service: Authentication service dependency
        
    Returns:
        ReturnUserDTO: Created user data
        
    Raises:
        HTTPException: 409 if user already exists, 500 on database error
    """
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
    """
    Authenticate user and return tokens.
    
    Args:
        user: User login credentials (email, password)
        auth_service: Authentication service dependency
        
    Returns:
        TokenSchema: Access and refresh tokens
        
    Raises:
        HTTPException: 401 on authentication error, 404 if user not found
    """
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
    """
    Refresh access token using refresh token.
    
    Args:
        token: Refresh token schema
        auth_service: Authentication service dependency
        
    Returns:
        TokenSchema: New access and refresh tokens
        
    Raises:
        HTTPException: 401 on invalid token error
    """
    try:
        return await auth_service.refresh_token(token.token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}",
        )
