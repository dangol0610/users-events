from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateEventDTO(BaseModel):
    title: str = Field(min_length=10, max_length=255)
    description: str = Field(min_length=10, max_length=255)

    model_config = ConfigDict(from_attributes=True)


class ReturnEventDTO(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
