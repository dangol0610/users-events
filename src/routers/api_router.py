from fastapi import APIRouter

from src.apps.auth.routers import auth_router
from src.apps.events.routers import event_router
from src.apps.users.routers import users_router

"""API роутер."""
router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(event_router)
