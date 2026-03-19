from datetime import datetime

from pydantic import BaseModel


class EventCreatedMessage(BaseModel):
    event_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


EVENT_CREATED_QUEUE = "events.created"
