from fastapi import APIRouter, HTTPException, status

from src.apps.auth.dependencies import CurrentUserDependency
from src.apps.events.dependencies import EventServiceDependency
from src.apps.events.schemas import CreateEventDTO, ReturnEventDTO
from src.utils.exceptions import DatabaseError

event_router = APIRouter(prefix="/events", tags=["Events"])


@event_router.get("/")
async def get_event(
    event_id: int,
    event_service: EventServiceDependency,
):
    pass


@event_router.post("/")
async def create_event(
    user: CurrentUserDependency,
    event_data: CreateEventDTO,
    event_service: EventServiceDependency,
) -> ReturnEventDTO:
    try:
        event = await event_service.create_event(event_data, user.id)
        return event
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )
