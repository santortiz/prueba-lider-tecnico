from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate
from app.utils.email import send_email

def create_reservation(db: Session, reservation: ReservationCreate):
    # Verificar que la mesa exista
    table = db.query(Table).filter(Table.id == reservation.table_id).first()
    if not table:
        raise ValueError("Table does not exist")

    # Verificar conflictos: misma mesa, fecha y hora
    existing = db.query(Reservation).filter(
        and_(
            Reservation.table_id == reservation.table_id,
            Reservation.date == reservation.date,
            Reservation.time == reservation.time,
            Reservation.status != "finished"  # Se permiten reservas pasadas finalizadas
        )
    ).first()

    if existing:
        raise ValueError("Table already reserved at this date and time")

    # Crear reserva
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)


    # Enviar email si hay dirección
    if db_reservation.notification_email:
        send_email(to_email=db_reservation.notification_email)

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
