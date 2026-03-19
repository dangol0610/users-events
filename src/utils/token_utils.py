from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from src.settings.settings import settings
from src.utils.exceptions import InvalidTokenError, InvalidTokenTypeError


class TokenUtils:
    """Класс утилит для работы с токенами."""

    @staticmethod
    def create_access_token(user_id: int, expires_minutes: int) -> str:
        """Создает токен доступа с заданными данными и временем истечения."""
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes)
        to_encode = {
            "sub": str(user_id),
            "iat": datetime.now(tz=timezone.utc),
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: int, expires_days: int) -> str:
        """Создает токен обновления с заданными данными и временем истечения."""
        expire = datetime.now(tz=timezone.utc) + timedelta(days=expires_days)
        to_encode = {
            "sub": str(user_id),
            "iat": datetime.now(tz=timezone.utc),
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> dict:
        """Декодирует токен доступа и возвращает полезную нагрузку."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=settings.ALGORITHM,
            )
            token_type = payload.get("type")
            if token_type != "access":
                raise InvalidTokenTypeError("Invalid token type")
        except JWTError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")
        return payload

    @staticmethod
    def decode_refresh_token(token: str) -> dict:
        """Декодирует токен обновления и возвращает полезную нагрузку."""
        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=settings.ALGORITHM,
            )
            token_type = payload.get("type")
            if token_type != "refresh":
                raise InvalidTokenTypeError("Invalid token type")
        except JWTError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")
        return payload
