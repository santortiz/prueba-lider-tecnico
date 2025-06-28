from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate

def create_reservation(db: Session, reservation: ReservationCreate):
    table = db.query(Table).filter(Table.id == reservation.table_id).first()
    if not table:
        raise ValueError("Table does not exist")

    # Verificar que no haya reserva en ese horario
    existing = db.query(Reservation).filter(
        and_(
            Reservation.table_id == reservation.table_id,
            Reservation.date == reservation.date,
            Reservation.time == reservation.time,
            Reservation.status != "finished"
        )
    ).first()

    if existing:
        raise ValueError("Table already reserved at this date and time")

    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservations(db: Session):
    return db.query(Reservation).all()

def get_reservation(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        db.delete(reservation)
        db.commit()
    return reservation
