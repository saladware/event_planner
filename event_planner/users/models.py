from sqlalchemy import Column, String, BigInteger

from event_planner.db import Base


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    telegram_id = Column(BigInteger)
    hashed_password = Column(String)
