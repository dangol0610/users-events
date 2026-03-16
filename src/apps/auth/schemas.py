from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    """Schema for user registration"""

    email: EmailStr
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=8, max_length=50)


class UserLoginSchema(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class TokenSchema(BaseModel):
    """Schema for returning a token"""

    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenSchema(BaseModel):
    """Schema for refreshing a token"""

    token: str
