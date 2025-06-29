# app/services/reservation_pool_service.py

from sqlalchemy.orm import Session
from app.models.reservation_pool import ReservationPool
from app.schemas.reservation_pool import ReservationPoolCreate

def add_to_pool(db: Session, data: ReservationPoolCreate):
    item = ReservationPool(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_by_date_and_time(db: Session, date, time):
    return db.query(ReservationPool).filter(
        ReservationPool.date == date,
        ReservationPool.time == time
    ).all()

def delete_all_by_date_and_time(db: Session, date, time):
    db.query(ReservationPool).filter(
        ReservationPool.date == date,
        ReservationPool.time == time
    ).delete()
    db.commit()
