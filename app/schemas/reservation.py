from pydantic import BaseModel
from datetime import date, time

class ReservationBase(BaseModel):
    table_id: int
    date: date
    time: time
    guests: int
    status: str = "reserved"
    notes: str | None = None

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    id: int

    class Config:
        orm_mode = True
