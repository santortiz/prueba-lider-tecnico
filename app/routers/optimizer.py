# app/routers/optimizer.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, time
from app.database import SessionLocal
from app.services import reservation_pool_service, table_service, reservation_service
from app.schemas.reservation import ReservationCreate
from app.dependencies.auth import require_role
from app.utils.optimizer import optimize_table_assignment

router = APIRouter(prefix="/optimize", tags=["Optimizer"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", dependencies=[Depends(require_role("admin"))])
def assign_reservations_optimally(
    date: date = Query(...),
    time: time = Query(...),
    db: Session = Depends(get_db)
):
    reservations = reservation_pool_service.get_by_date_and_time(db, date, time)
    tables = table_service.get_tables(db)

    # Filtrar mesas libres y sin conflicto
    available_tables = [
        t for t in tables
        if t.status == "free" and not any(
            r.date == date and r.time == time and r.table_id == t.id
            for r in t.reservations
        )
    ]

    # Entradas para el modelo
    res_data = [(r.id, r.guests) for r in reservations]
    tab_data = [(t.id, t.capacity) for t in available_tables]

    assignments = optimize_table_assignment(res_data, tab_data)

    if not assignments:
        raise HTTPException(status_code=400, detail="No optimal assignment found")

    successful = []
    failed = []

    reservation_lookup = {r.id: r for r in reservations}

    for a in assignments:
        original = reservation_lookup[a["reservation_id"]]
        try:
            reservation_service.create_automatic_reservation(db, ReservationCreate(
                table_id=a["table_id"],
                guests=a["guests"],
                date=date,
                time=time,
                notes="(From pool) " + (original.notes or ""),
                notification_email=original.notification_email
            ))
            successful.append(a["reservation_id"])
        except Exception as e:
            print(f"❌ No se pudo asignar reserva {a['reservation_id']} a mesa {a['table_id']}: {e}")
            failed.append(a["reservation_id"])

    # Eliminar solo las reservas exitosamente asignadas del pool
    for r_id in successful:
        db.query(reservation_pool_service.ReservationPool).filter_by(id=r_id).delete()
    db.commit()

    return {
        "assigned": [a for a in assignments if a["reservation_id"] in successful],
        "unassigned": [a for a in assignments if a["reservation_id"] in failed],
    }