from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import staff_service, room_service, table_service, reservation_service
from app.schemas.staff import StaffCreate
from app.schemas.room import RoomCreate
from app.schemas.table import TableCreate
from app.schemas.reservation import ReservationCreate
from datetime import date, time



def seed_data():
    db: Session = SessionLocal()
    try:
        # Seed staff
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

        # Seed rooms
        room_names = ["Interior", "Terraza"]
        room_ids = {}

        for name in room_names:
            room = next((r for r in room_service.get_rooms(db) if r.name == name), None)
            if not room:
                room = room_service.create_room(db, RoomCreate(name=name, description=f"Salón {name}"))
            room_ids[name] = room.id

        # Seed tables
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

        # Seed reservation (opcional)
        today = date.today()
        reservation_time = time(hour=19, minute=0)

        reservation_service.create_automatic_reservation(db, ReservationCreate(
            date=today,
            time=reservation_time,
            guests=2,
            notes="Reserva demo",
            notification_email="cliente@demo.com"
        ))

        print("✅ Seed data inserted")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()