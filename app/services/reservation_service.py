from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from app.utils.email import send_email
from app.services.table_service import find_best_table


def create_automatic_reservation(db: Session, reservation: ReservationCreate):
    # Redondear la hora ya fue hecho en el schema
    guests = reservation.guests
    date = reservation.date
    time = reservation.time

    table_id = reservation.table_id

    if not table_id:
        table = find_best_table(db, date, time, guests)
        if not table:
            raise ValueError("No available table for that time and number of guests")
        table_id = table.id

    # Verifica conflicto
    existing = db.query(Reservation).filter(
        and_(
            Reservation.table_id == table_id,
            Reservation.date == date,
            Reservation.time == time,
            Reservation.status != "finished"
        )
    ).first()

    if existing:
        raise ValueError("Table already reserved at this date and time")

    db_reservation = Reservation(
        table_id=table_id,
        date=date,
        time=time,
        guests=guests,
        notes=reservation.notes,
        status=reservation.status,
        notification_email=reservation.notification_email
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    #enviar email de confirmación si registran email
    if db_reservation.notification_email:
        send_email(
            to_email=db_reservation.notification_email
        )

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

def mark_as_occupied(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise ValueError("Reservation not found")

    reservation.status = "occupied"
    reservation.table.status = "occupied"  # sincroniza estado de mesa
    db.commit()
    db.refresh(reservation)
    return reservation

def mark_as_finished(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise ValueError("Reservation not found")

    reservation.status = "finished"
    reservation.table.status = "free"  # libera mesa
    db.commit()
    db.refresh(reservation)
    return reservation
