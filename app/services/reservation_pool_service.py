from sqlalchemy.orm import Session
from app.models.reservation_pool import ReservationPool
from app.schemas.reservation_pool import ReservationPoolCreate, ReservationPoolBase

def add_to_pool(db: Session, data: ReservationPoolCreate):
    item = ReservationPool(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_by_id(db: Session, id: int):
    return db.query(ReservationPool).filter(ReservationPool.id == id).first()

def get_all(db: Session):
    return db.query(ReservationPool).all()

def get_by_date_and_time(db: Session, date, time):
    return db.query(ReservationPool).filter(
        ReservationPool.date == date,
        ReservationPool.time == time
    ).all()

def update_pool_item(db: Session, id: int, data: ReservationPoolBase):
    item = get_by_id(db, id)
    if not item:
        return None
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_by_id(db: Session, id: int):
    item = get_by_id(db, id)
    if item:
        db.delete(item)
        db.commit()
    return item
