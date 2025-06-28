from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.reservation import ReservationCreate, ReservationOut
from app.services import reservation_service
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/reservations", tags=["Reservations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReservationOut, dependencies=[Depends(require_role("admin"))])
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:
        return reservation_service.create_reservation(db, reservation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ReservationOut], dependencies=[Depends(get_current_user)])
def read_reservations(db: Session = Depends(get_db)):
    return reservation_service.get_reservations(db)

@router.get("/{reservation_id}", response_model=ReservationOut, dependencies=[Depends(get_current_user)])
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = reservation_service.get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.delete("/{reservation_id}", response_model=ReservationOut, dependencies=[Depends(require_role("admin"))])
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = reservation_service.delete_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@router.post("/{reservation_id}/arrive", response_model=ReservationOut, dependencies=[Depends(get_current_user)])
def arrive_reservation(reservation_id: int, db: Session = Depends(get_db)):
    try:
        return reservation_service.mark_as_occupied(db, reservation_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{reservation_id}/finish", response_model=ReservationOut, dependencies=[Depends(get_current_user)])
def finish_reservation(reservation_id: int, db: Session = Depends(get_db)):
    try:
        return reservation_service.mark_as_finished(db, reservation_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
