from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.table import TableCreate, TableOut
from app.services import table_service

router = APIRouter(prefix="/tables", tags=["Tables"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TableOut)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    try:
        return table_service.create_table(db, table)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TableOut])
def read_tables(db: Session = Depends(get_db)):
    return table_service.get_tables(db)

@router.get("/{table_id}", response_model=TableOut)
def read_table(table_id: int, db: Session = Depends(get_db)):
    table = table_service.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.delete("/{table_id}", response_model=TableOut)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = table_service.delete_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table
