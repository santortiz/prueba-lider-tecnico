from sqlalchemy import Column, Integer, String
from app.database import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    room = Column(String, index=True)
    capacity = Column(Integer)
    status = Column(String, default="free")  # free, reserved, occupied
