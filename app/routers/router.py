from fastapi import APIRouter

from app.routers import (
    healthcheck,
    table
)

router = APIRouter()

router.include_router(healthcheck.router, prefix="/health", tags=["Healthcheck"])
router.include_router(table.router, prefix="/tables", tags=["Tables"])
