from pydantic import BaseModel
from datetime import datetime


class BaseEvent(BaseModel):
    name: str
    description: str
    planned_at: datetime


class CreateEvent(BaseEvent):
    ...


class UpdateEvent(BaseEvent):
    name: str | None
    description: str | None
    planned_at: datetime | None


class Event(BaseEvent):
    id: int
    author_id: str

    class Config:
        orm_mode = True
