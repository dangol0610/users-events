from loguru import logger

from src.apps.auth.schemas import (
    RefreshTokenSchema,
    TokenSchema,
    UserLoginSchema,
    UserRegisterSchema,
)
from src.apps.users.schemas import CreateUserDTO, ReturnUserDTO
from src.settings.settings import settings
from src.utils.exceptions import (
    AuthenticationError,
    DatabaseError,
    InvalidTokenError,
    NotFoundError,
    UserAlreadyExistsError,
)
from src.utils.pwd_utils import PasswordUtils
from src.utils.token_utils import TokenUtils


class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    async def register(self, user: UserRegisterSchema) -> ReturnUserDTO:
        """Register a new user."""
        try:
            hashed_password = PasswordUtils.hash_password(user.password)
            logger.info("Password hashed successfully")

            user_data = CreateUserDTO(
                email=user.email,
                username=user.username,
                hashed_password=hashed_password,
            )
            created_user = await self.user_service.create_user(user_data)
            logger.info(f"User created successfully with id: {created_user.id}")
            return created_user
        except (UserAlreadyExistsError, DatabaseError):
            logger.exception("Failed to register user")
            raise

    async def login(self, user_data: UserLoginSchema) -> TokenSchema:
        """Login a user."""
        try:
            user = await self.user_service.authenticate(
                email=user_data.email, password=user_data.password
            )
            logger.info(f"User authenticated successfully: {user.email}")
            access = TokenUtils.create_access_token(
                user.id, expires_minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
            )
            refresh = TokenUtils.create_refresh_token(
                user.id, expires_days=settings.REFRESH_TOKEN_EXPIRES_DAYS
            )
            logger.info(f"Access token created for user: {user.email}")
            logger.info(f"Refresh token created for user: {user.email}")
            return TokenSchema(
                access_token=access, refresh_token=refresh, token_type="bearer"
            )
        except (AuthenticationError, NotFoundError):
            logger.exception("Failed to login user")
            raise

    async def refresh_token(self, refresh_token: RefreshTokenSchema) -> TokenSchema:
        """Refresh an access token using a refresh token."""
        try:
            payload = TokenUtils.decode_refresh_token(refresh_token)
            user_id = payload.get("sub")
            if not user_id:
                raise InvalidTokenError("Invalid token: missing user ID")

            access = TokenUtils.create_access_token(
                user_id, expires_minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
            )
            refresh = TokenUtils.create_refresh_token(
                user_id, expires_days=settings.REFRESH_TOKEN_EXPIRES_DAYS
            )
            return TokenSchema(
                access_token=access, refresh_token=refresh, token_type="bearer"
            )
        except InvalidTokenError as e:
            logger.exception("Failed to refresh token")
            raise InvalidTokenError(str(e))
