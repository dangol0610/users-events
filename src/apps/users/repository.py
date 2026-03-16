from loguru import logger
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.models import User
from src.apps.users.schemas import CreateUserDTO, UpdateUserDTO


class UserRepository:
    """Repository for user operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        try:
            query = select(User).where(User.email == email)
            result = await self.session.execute(query)
            user_result = result.scalar_one_or_none()
            if not user_result:
                return None
            return user_result
        except SQLAlchemyError:
            logger.exception("Failed to get user by email")
            raise

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by id."""
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user_result = result.scalar_one_or_none()
            if not user_result:
                return None
            return user_result
        except SQLAlchemyError:
            logger.exception("Failed to get user by id")
            raise

    async def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        try:
            query = select(User).where(User.username == username)
            result = await self.session.execute(query)
            user_result = result.scalar_one_or_none()
            if not user_result:
                return None
            return user_result
        except SQLAlchemyError:
            logger.exception("Failed to get user by username")
            raise

    async def create_user(self, user_data: CreateUserDTO):
        """Create a new user."""
        try:
            user_to_insert = user_data.model_dump()
            stmt = insert(User).values(user_to_insert).returning(User)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError:
            logger.exception("Failed to create user")
            raise

    async def update_user(self, user_id: int, user: UpdateUserDTO):
        """Update a user."""
        try:
            query = select(User).where(User.id == user_id)
            user_to_update = await self.session.execute(query)
            user_to_update = user_to_update.scalar_one_or_none()
            if not user_to_update:
                logger.exception("Failed to update user: user not found")
                return None
            user_data = user.model_dump(exclude_unset=True)
            stmt = (
                update(User).where(User.id == user_id).values(user_data).returning(User)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError:
            logger.exception("Failed to update user")
            await self.session.rollback()
            raise

    async def delete_user(self, user_id: int):
        """Delete a user."""
        try:
            query = select(User).where(User.id == user_id)
            user_to_delete = await self.session.execute(query)
            user_to_delete = user_to_delete.scalar_one_or_none()
            if not user_to_delete:
                logger.exception("Failed to delete user: user not found")
                return None
            stmt = delete(User).where(User.id == user_id).returning(User)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError:
            logger.exception("Failed to delete user")
            await self.session.rollback()
            raise
