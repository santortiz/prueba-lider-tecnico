from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import RoomCreate

def create_room(db: Session, room: RoomCreate):
    db_room = Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms(db: Session):
    return db.query(Room).all()

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room:
        db.delete(room)
        db.commit()
    return room