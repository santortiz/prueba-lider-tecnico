from fastapi import APIRouter

from app.routers import (
    healthcheck
)

router = APIRouter()

router.include_router(healthcheck.router, prefix="/health", tags=["Healthcheck"])
