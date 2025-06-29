from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from app.utils.email import send_email
from app.services.table_service import find_best_table


def create_automatic_reservation(db: Session, reservation: ReservationCreate):
    """
    Creates an automatic reservation for a table in the database.

    Parameters
    ----------
    db : Session
        The database session used to interact with the database.
    reservation : ReservationCreate
        The reservation details, including guests, date, time, table ID, and other optional fields.

    Returns
    -------
    Reservation
        The created reservation object.

    Raises
    ------
    ValueError
        If no table is available for the specified time and number of guests.
        If the table ID is not provided for reservations with more than 6 guests.
        If the table is already reserved at the specified date and time.

    Notes
    -----
    - If the `table_id` is not provided and the number of guests is less than or equal to 6, 
      the function attempts to find the best available table.
    - If a notification email is provided in the reservation details, a confirmation email 
      will be sent after the reservation is created.
    """
    # Redondear la hora ya fue hecho en el schema
    guests = reservation.guests
    date = reservation.date
    time = reservation.time

    table_id = reservation.table_id

    if not table_id and guests <= 6:
        table = find_best_table(db, date, time, guests)
        if not table:
            raise ValueError("No available table for that time and number of guests")
        table_id = table.id
    elif not table_id:
        raise ValueError("Table ID must be provided for reservations with more than 6 guests")

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
