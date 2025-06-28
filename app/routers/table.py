from datetime import date as dt_date, time as dt_time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.table import TableCreate, TableOut
from app.services import table_service
from app.dependencies.auth import get_current_user, require_role
from app.services.table_service import get_available_tables_by_room

router = APIRouter(prefix="/tables", tags=["Tables"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TableOut, dependencies=[Depends(require_role("admin"))])
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    try:
        return table_service.create_table(db, table)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TableOut], dependencies=[Depends(get_current_user)])
def read_tables(db: Session = Depends(get_db)):
    return table_service.get_tables(db)

@router.get("/available-by-room")
def get_tables_by_room(
    guests: int = Query(..., gt=6),
    date: dt_date = Query(...),
    time: dt_time = Query(...),
    db: Session = Depends(get_db),
    _ = Depends(get_current_user)
):
    return get_available_tables_by_room(db, date, time, guests)

@router.get("/{table_id}", response_model=TableOut, dependencies=[Depends(get_current_user)])
def read_table(table_id: int, db: Session = Depends(get_db)):
    table = table_service.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.delete("/{table_id}", response_model=TableOut, dependencies=[Depends(require_role("admin"))])
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = table_service.delete_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.post("/{table_id}/occupy", response_model=TableOut, dependencies=[Depends(get_current_user)])
def occupy_table(table_id: int, db: Session = Depends(get_db)):
    try:
        return table_service.mark_table_as_occupied(db, table_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{table_id}/free", response_model=TableOut, dependencies=[Depends(get_current_user)])
def free_table(table_id: int, db: Session = Depends(get_db)):
    try:
        return table_service.mark_table_as_free(db, table_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


