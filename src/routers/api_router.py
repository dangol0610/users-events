from fastapi import APIRouter

from src.apps.auth.routers import auth_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
