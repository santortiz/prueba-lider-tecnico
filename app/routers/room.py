from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.room import RoomCreate, RoomOut
from app.services import room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RoomOut)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return room_service.create_room(db, room)

@router.get("/", response_model=list[RoomOut])
def read_rooms(db: Session = Depends(get_db)):
    return room_service.get_rooms(db)

@router.get("/{room_id}", response_model=RoomOut)
def read_room(room_id: int, db: Session = Depends(get_db)):
    room = room_service.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/{room_id}", response_model=RoomOut)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = room_service.delete_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room
