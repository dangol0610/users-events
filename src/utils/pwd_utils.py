from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    """Класс утилит для работы с паролями."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Хэширует пароль с использованием bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Проверяет пароль на соответствие хэшу."""
        return pwd_context.verify(password, hashed_password)
