from pydantic import BaseModel
from datetime import datetime


class BaseEvent(BaseModel):
    name: str
    description: str
    planned_at: datetime
    remind_at: datetime | None


class CreateEvent(BaseEvent):
    ...


class UpdateEvent(BaseEvent):
    name: str | None
    description: str | None
    planned_at: datetime | None
    remind_at: datetime | None


class Event(BaseEvent):
    id: int
    author_id: str
    created_at: datetime
    is_happened: bool

    class Config:
        orm_mode = True


class EventList(BaseModel):
    events: list[Event]
