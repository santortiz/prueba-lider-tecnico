from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.staff import StaffCreate, StaffOut
from app.services import staff_service
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/staff", tags=["Staff"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=StaffOut, dependencies=[Depends(require_role("admin"))])
def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    if staff_service.get_staff_by_email(db, staff.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return staff_service.create_staff(db, staff)

@router.get("/", response_model=list[StaffOut], dependencies=[Depends(get_current_user)])
def list_staff(db: Session = Depends(get_db)):
    return staff_service.get_all_staff(db)
