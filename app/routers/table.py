from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.table import TableCreate, TableOut
from app.services import table_service
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TableOut)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    return table_service.create_table(db, table)

@router.get("/", response_model=list[TableOut])
def read_tables(db: Session = Depends(get_db)):
    return table_service.get_tables(db)