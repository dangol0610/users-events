from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from src.settings.settings import settings


class TokenUtils:
    @staticmethod
    def create_access_token(user_id: int, expires_minutes: int) -> str:
        """Creates an access token with the given data and expiration time."""
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
        """Creates a refresh token with the given data and expiration time."""
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
        """Decodes the given token and returns the payload."""
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            token_type = payload.get("type")
            if token_type == "refresh":
                raise JWTError("Invalid token type")
        except JWTError:
            raise JWTError("Invalid token")
        return payload
