from sqlalchemy.orm import Session
from app.models.table import Table
from app.models.room import Room
from app.models.reservation import Reservation
from app.schemas.table import TableCreate

from datetime import datetime, time
from sqlalchemy import and_


def create_table(db: Session, table: TableCreate):
    room = db.query(Room).filter(Room.id == table.room_id).first()
    if not room:
        raise ValueError("Room does not exist")
    db_table = Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_tables(db: Session):
    return db.query(Table).all()

def get_table(db: Session, table_id: int):
    return db.query(Table).filter(Table.id == table_id).first()

def delete_table(db: Session, table_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    if table:
        db.delete(table)
        db.commit()
    return table

def mark_table_as_occupied(db: Session, table_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise ValueError("Table not found")
    if table.status != "free":
        raise ValueError("Table is not available")

    now = datetime.now()
    today = now.date()
    current_hour = time(hour=now.hour)
    next_hour = time(hour=(now.hour + 1) % 24)  # soporta rollover 23 → 0

    conflict = db.query(Reservation).filter(
        and_(
            Reservation.table_id == table_id,
            Reservation.date == today,
            Reservation.time.in_([current_hour, next_hour]),
            Reservation.status.in_(["reserved", "occupied"])
        )
    ).first()

    if conflict:
        raise ValueError("Table has a reservation at this or next hour")

    table.status = "occupied"
    db.commit()
    db.refresh(table)
    return table

def mark_table_as_free(db: Session, table_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise ValueError("Table not found")

    table.status = "free"
    db.commit()
    db.refresh(table)
    return table