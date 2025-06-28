from fastapi import APIRouter

from app.routers import (
    healthcheck,
    table,
    room,
    reservation,
    staff,
    auth
)

router = APIRouter()

router.include_router(healthcheck.router, prefix="/health", tags=["Healthcheck"])
router.include_router(table.router, prefix="/tables", tags=["Tables"])
router.include_router(room.router, prefix="/rooms", tags=["Rooms"])
router.include_router(reservation.router, prefix="/reservations", tags=["Reservations"])
router.include_router(staff.router, prefix="/staff", tags=["Staff"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])