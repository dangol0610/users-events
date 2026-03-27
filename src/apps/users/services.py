from loguru import logger
from redis.asyncio import Redis, RedisError
from sqlalchemy.exc import SQLAlchemyError

from src.apps.users.models import User
from src.apps.users.repository import UserRepository
from src.apps.users.schemas import CreateUserDTO, ReturnUserDTO, UpdateUserDTO
from src.apps.users.tasks import send_welcome_email
from src.settings.settings import settings
from src.utils.exceptions import (
    AuthenticationError,
    CacheError,
    DatabaseError,
    NotFoundError,
    UserAlreadyExistsError,
)
from src.utils.pwd_utils import PasswordUtils


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, repository: UserRepository, redis: Redis):
        self.repository = repository
        self.redis = redis
        self.cache_ttl = settings.CACHE_TTL

    async def create_user(self, user_data: CreateUserDTO) -> ReturnUserDTO:
        """Создать нового пользователя."""
        try:
            existing_user_by_email = await self.repository.get_user_by_email(
                user_data.email
            )
            if existing_user_by_email:
                logger.info(f"User {user_data.email} already exists")
                raise UserAlreadyExistsError

            existing_user_by_username = await self.repository.get_user_by_username(
                user_data.username
            )
            if existing_user_by_username:
                logger.info(f"User {user_data.username} already exists")
                raise UserAlreadyExistsError

            user_from_db = await self.repository.create_user(user_data)
            logger.info(f"User created with id: {user_from_db.id}")
            return ReturnUserDTO.model_validate(user_from_db)
        except SQLAlchemyError:
            logger.exception("SQLAlchemy error while creating user")
            raise DatabaseError

    async def get_user_by_id(self, user_id: int) -> ReturnUserDTO | None:
        """Получить пользователя по ID."""
        try:
            cached_user = await self.redis.get(f"user:{user_id}")
            if cached_user:
                logger.info(f"User {user_id} found in cache")
                return ReturnUserDTO.model_validate_json(cached_user)
            user_from_db = await self.repository.get_user_by_id(user_id)
            if not user_from_db:
                logger.info(f"User {user_id} not found in cache and database")
                raise NotFoundError
            user = ReturnUserDTO.model_validate(user_from_db)
            await self.redis.set(
                f"user:{user_id}", user.model_dump_json(), ex=self.cache_ttl
            )
            logger.info(f"User {user_id} cached")
            return user
        except RedisError:
            logger.exception(f"Redis error while caching user {user_id}")
            raise CacheError
        except SQLAlchemyError:
            logger.exception(f"SQLAlchemy error while getting user {user_id}")
            raise DatabaseError

    async def get_user_by_email(self, email: str) -> ReturnUserDTO | None:
        """Получить пользователя по email."""
        try:
            user_from_db = await self.repository.get_user_by_email(email)
            if not user_from_db:
                logger.info(f"User {email} not found in database")
                raise NotFoundError
            logger.info(f"User {email} found in database")
            return ReturnUserDTO.model_validate(user_from_db)
        except SQLAlchemyError:
            logger.exception(f"SQLAlchemy error while getting user {email}")
            raise DatabaseError

    async def get_user_by_username(self, username: str) -> ReturnUserDTO | None:
        """Получить пользователя по username."""
        try:
            user_from_db = await self.repository.get_user_by_username(username)
            if not user_from_db:
                logger.info(f"User {username} not found in database")
                raise NotFoundError
            logger.info(f"User {username} found in database")
            return ReturnUserDTO.model_validate(user_from_db)
        except SQLAlchemyError:
            logger.exception(f"SQLAlchemy error while getting user {username}")
            raise DatabaseError

    async def update_user(
        self, user_id: int, user_data: UpdateUserDTO
    ) -> ReturnUserDTO:
        """Обновить пользователя."""
        try:
            updated_user = await self.repository.update_user(user_id, user_data)
            if not updated_user:
                logger.info(f"User {user_id} not found in database")
                raise NotFoundError
            logger.info(f"User {user_id} updated in database")
            user = ReturnUserDTO.model_validate(updated_user)
            await self.redis.set(
                f"user:{user_id}", user.model_dump_json(), ex=self.cache_ttl
            )
            return user
        except RedisError:
            logger.exception(f"Redis error while caching user {user_id}")
            raise CacheError
        except SQLAlchemyError:
            logger.exception(f"SQLAlchemy error while getting user {user_id}")
            raise DatabaseError

    async def delete_user(self, user_id: int) -> ReturnUserDTO:
        """Удалить пользователя."""
        try:
            user = await self.repository.delete_user(user_id)
            if not user:
                logger.info(f"User {user_id} not found in database")
                raise NotFoundError
            logger.info(f"User {user_id} deleted from database")
            await self.redis.delete(f"user:{user_id}")
            logger.info(f"User {user_id} deleted from cache")
            return ReturnUserDTO.model_validate(user)
        except RedisError:
            logger.exception(f"Redis error while deleting user {user_id} from cache")
            raise CacheError
        except SQLAlchemyError:
            logger.exception(f"SQLAlchemy error while deleting user {user_id}")
            raise DatabaseError

    async def authenticate(self, email: str, password: str) -> User:
        """Аутентифицировать пользователя по email и паролю."""
        user = await self.repository.get_user_by_email(email)
        if not user:
            logger.info(f"User with email {email} not found in database")
            raise NotFoundError
        logger.info(f"User found for email {email}")
        if not PasswordUtils.verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password for user {email}")
            raise AuthenticationError("Invalid email or password")
        logger.info(f"Authentication successful for user {email}")
        return user
