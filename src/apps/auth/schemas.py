from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    """Схема для регистрации пользователя"""

    email: EmailStr
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=8, max_length=50)


class UserLoginSchema(BaseModel):
    """Схема для входа пользователя"""

    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class TokenSchema(BaseModel):
    """Схема для возврата токена"""

    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenSchema(BaseModel):
    """Схема для обновления токена"""

    token: str
