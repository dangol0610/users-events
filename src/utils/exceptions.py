class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class InvalidTokenError(Exception):
    """Raised when an invalid token is provided."""

    pass


class InvalidTokenTypeError(Exception):
    """Raised when an invalid token type is provided."""

    pass


class CredentialsMissingError(Exception):
    """Raised when credentials are missing."""

    pass


class DatabaseError(Exception):
    """Raised when a database error occurs."""

    pass


class FastStreamError(Exception):
    """Raised when a FastStream error occurs."""

    pass


class NotFoundError(Exception):
    """Raised when a resource is not found."""

    pass


class CacheError(Exception):
    """Raised when a cache error occurs."""

    pass


class UserAlreadyExistsError(Exception):
    """Raised when a user already exists."""

    pass
