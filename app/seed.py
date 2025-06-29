from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import (
    staff_service,
    room_service,
    table_service,
    reservation_service,
)
from app.schemas.staff import StaffCreate
from app.schemas.room import RoomCreate
from app.schemas.table import TableCreate
from app.schemas.reservation import ReservationCreate
from datetime import date, time

# NUEVO
from app.models.reservation_pool import ReservationPool

def seed_data():
    db: Session = SessionLocal()
    try:
        # =======================
        # Staff
        # =======================
        if not staff_service.get_staff_by_email(db, "admin@resto.com"):
            staff_service.create_staff(db, StaffCreate(
                full_name="Admin User",
                email="admin@resto.com",
                role="admin",
                password="admin123"
            ))

        if not staff_service.get_staff_by_email(db, "waiter@resto.com"):
            staff_service.create_staff(db, StaffCreate(
                full_name="Waiter User",
                email="waiter@resto.com",
                role="waiter",
                password="waiter123"
            ))

        # =======================
        # Rooms
        # =======================
        room_names = ["Interior", "Terraza"]
        room_ids = {}

        for name in room_names:
            room = next((r for r in room_service.get_rooms(db) if r.name == name), None)
            if not room:
                room = room_service.create_room(db, RoomCreate(name=name, description=f"Salón {name}"))
            room_ids[name] = room.id

        # =======================
        # Tables
        # =======================
        predefined_tables = [
            {"room": "Interior", "capacity": 2},
            {"room": "Interior", "capacity": 4},
            {"room": "Interior", "capacity": 6},
            {"room": "Interior", "capacity": 10},
            {"room": "Terraza", "capacity": 2},
            {"room": "Terraza", "capacity": 4},
            {"room": "Terraza", "capacity": 8},
            {"room": "Terraza", "capacity": 10}
        ]

        existing_tables = table_service.get_tables(db)
        for tbl in predefined_tables:
            if not any(t.capacity == tbl["capacity"] and t.room_id == room_ids[tbl["room"]] for t in existing_tables):
                table_service.create_table(db, TableCreate(
                    room_id=room_ids[tbl["room"]],
                    capacity=tbl["capacity"],
                    status="free"
                ))

        # =======================
        # Reserva asignada de ejemplo
        # =======================
        today = date.today()
        reservation_time = time(hour=19, minute=0)

        try:
            reservation_service.create_automatic_reservation(db, ReservationCreate(
                date=today,
                time=time(hour=19, minute=0),
                guests=2,
                notes="Reserva demo",
                notification_email="cliente@demo.com"
            ))
        except Exception:
            pass  # Por si ya está creada

        # =======================
        # POOL: Reservas sin asignar para optimización
        # =======================
        db.query(ReservationPool).delete()

        perfect_pool = [
            (2, None),
            (2, None),
            (4, None),
            (4, None),
            (6, None),
            (8, None),
            (10, None),
            (10, None),
        ]

        pool_reservations = [
            ReservationPool(
                date=today,
                time=reservation_time,
                guests=guests,
                notes=f"Reserva óptima {guests}",
                notification_email=email
            )
            for guests, email in perfect_pool
        ]

        db.add_all(pool_reservations)
        db.commit()


        print("✅ Seed data inserted (reservations + pool)")
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()
