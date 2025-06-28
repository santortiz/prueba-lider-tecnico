from sqlalchemy.orm import Session
from app.models.staff import Staff
from app.schemas.staff import StaffCreate
from app.utils.auth import hash_password

def create_staff(db: Session, staff: StaffCreate):
    db_staff = Staff(
        full_name=staff.full_name,
        email=staff.email,
        role=staff.role,
        hashed_password=hash_password(staff.password)
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def get_staff_by_email(db: Session, email: str):
    return db.query(Staff).filter(Staff.email == email).first()

def get_all_staff(db: Session):
    return db.query(Staff).all()
