from pydantic import BaseModel, field_validator
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
        from_attributes = True

class ReservationCreate(ReservationBase):

    @field_validator("time", mode="before")
    def truncate_minutes(cls, value):
        """
        Convierte la hora ingresada a la hora en punto más cercana hacia abajo.
        Ej: 14:26:14 => 14:00
        """
        if isinstance(value, str):
            hour = int(value.split(":")[0])
            return time(hour, 0)
        elif isinstance(value, time):
            return time(value.hour, 0)
        return value