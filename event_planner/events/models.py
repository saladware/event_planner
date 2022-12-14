import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

from ..db import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    remind_at: datetime.datetime = Column(DateTime)
    planned_at = Column(DateTime)
    author_id = Column(String, ForeignKey("users.username"))
    author = relationship("User")
    is_happened = Column(Boolean, default=False)



