from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes the given password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifies the given password against the hashed password."""
        return pwd_context.verify(password, hashed_password)
