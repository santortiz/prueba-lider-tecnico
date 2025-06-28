from sqlalchemy.orm import Session
from app.models.table import Table
from app.schemas.table import TableCreate

def create_table(db: Session, table: TableCreate):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_tables(db: Session):
    return db.query(Table).all()
