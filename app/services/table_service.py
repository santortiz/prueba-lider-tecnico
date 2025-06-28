from sqlalchemy.orm import Session
from app.models.table import Table
from app.models.room import Room
from app.schemas.table import TableCreate

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
