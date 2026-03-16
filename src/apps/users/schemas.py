from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserDTO(BaseModel):
    """Schema for creating a user"""

    email: EmailStr
    username: str = Field(min_length=5, max_length=50)
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class ReturnUserDTO(BaseModel):
    """Schema for returning a user"""

    id: int
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserDTO(BaseModel):
    """Schema for updating a user"""

    email: EmailStr | None = None
    username: str | None = None

    model_config = ConfigDict(from_attributes=True)
