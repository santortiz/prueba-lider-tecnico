from pydantic import BaseModel

class RoomBase(BaseModel):
    name: str
    description: str | None = None

class RoomCreate(RoomBase):
    pass

class RoomOut(RoomBase):
    id: int

    class Config:
        orm_mode = True