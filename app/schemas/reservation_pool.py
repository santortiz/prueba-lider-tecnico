# app/schemas/reservation_pool.py

from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class ReservationPoolBase(BaseModel):
    date: date
    time: time
    guests: int
    notes: Optional[str] = None
    notification_email: Optional[str] = None

class ReservationPoolCreate(ReservationPoolBase):
    pass

class ReservationPoolOut(ReservationPoolBase):
    id: int

    class Config:
        from_attributes = True
