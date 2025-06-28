from pydantic import BaseModel

class TableBase(BaseModel):
    room_id: int
    capacity: int
    status: str = "free"

class TableCreate(TableBase):
    pass

class TableOut(TableBase):
    id: int

    class Config:
        from_attributes = True
