from fastapi import APIRouter, HTTPException, status

from src.apps.auth.dependencies import CurrentUserDependency
from src.apps.events.dependencies import EventServiceDependency
from src.apps.events.schemas import CreateEventDTO, ReturnEventDTO
from src.utils.exceptions import CacheError, DatabaseError, FastStreamError

event_router = APIRouter(prefix="/events", tags=["Events"])


@event_router.post("/")
async def create_event(
    user: CurrentUserDependency,
    event_data: CreateEventDTO,
    event_service: EventServiceDependency,
) -> ReturnEventDTO:
    """Создание нового события."""
    try:
        event = await event_service.create_event(event_data, user.id)
        return event
    except (DatabaseError, FastStreamError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@event_router.get("/")
async def get_event_by_user(
    user: CurrentUserDependency,
    event_service: EventServiceDependency,
) -> list[ReturnEventDTO]:
    """Получение всех событий пользователя."""
    try:
        events = await event_service.get_event_by_user(user.id)
        return events
    except (DatabaseError, CacheError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )
