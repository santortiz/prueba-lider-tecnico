from fastapi import APIRouter

from app.routers import (
    healthcheck,
    table,
    room,
    reservation
)

router = APIRouter()

router.include_router(healthcheck.router, prefix="/health", tags=["Healthcheck"])
router.include_router(table.router, prefix="/tables", tags=["Tables"])
router.include_router(room.router, prefix="/rooms", tags=["Rooms"])
router.include_router(reservation.router, prefix="/reservations", tags=["Reservations"])