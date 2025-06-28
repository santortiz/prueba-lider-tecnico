from pydantic import BaseModel

class StaffBase(BaseModel):
    full_name: str
    email: str
    role: str # "waiter" or "admin"

class StaffCreate(StaffBase):
    password: str

class StaffOut(StaffBase):
    id: int

    class Config:
        from_attributes = True
