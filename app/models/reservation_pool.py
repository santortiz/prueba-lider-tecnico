# app/models/reservation_pool.py

from sqlalchemy import Column, Integer, String, Date, Time
from app.database import Base

class ReservationPool(Base):
    __tablename__ = "reservation_pool"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    guests = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    notification_email = Column(String, nullable=True)