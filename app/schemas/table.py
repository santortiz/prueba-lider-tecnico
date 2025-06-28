from pydantic import BaseModel

class TableBase(BaseModel):
    room: str
    capacity: int
    status: str = "free"

class TableCreate(TableBase):
    pass

class TableOut(TableBase):
    id: int

    class Config:
        from_attributes = True
    