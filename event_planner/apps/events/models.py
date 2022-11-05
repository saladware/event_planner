from ...db import Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    planned_at = Column(DateTime)