from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.reservation_pool import ReservationPoolCreate, ReservationPoolOut, ReservationPoolBase
from app.services import reservation_pool_service
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/reservation-pool", tags=["Reservation Pool"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReservationPoolOut, dependencies=[Depends(get_current_user)])
def create_pool_item(item: ReservationPoolCreate, db: Session = Depends(get_db)):
    return reservation_pool_service.add_to_pool(db, item)

@router.get("/", response_model=list[ReservationPoolOut], dependencies=[Depends(get_current_user)])
def list_all_pool_items(db: Session = Depends(get_db)):
    return reservation_pool_service.get_all(db)

@router.get("/{item_id}", response_model=ReservationPoolOut, dependencies=[Depends(get_current_user)])
def get_pool_item(item_id: int, db: Session = Depends(get_db)):
    item = reservation_pool_service.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return item

@router.put("/{item_id}", response_model=ReservationPoolOut, dependencies=[Depends(get_current_user)])
def update_pool_item(item_id: int, data: ReservationPoolBase, db: Session = Depends(get_db)):
    item = reservation_pool_service.update_pool_item(db, item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return item

@router.delete("/{item_id}", response_model=ReservationPoolOut, dependencies=[Depends(require_role("admin"))])
def delete_pool_item(item_id: int, db: Session = Depends(get_db)):
    item = reservation_pool_service.delete_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return item