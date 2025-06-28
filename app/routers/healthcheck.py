from fastapi import APIRouter
from app.services.healthcheck_service import check_api

router = APIRouter()

@router.get("/health", tags=["Healthcheck"])
def healthcheck():
    return check_api()