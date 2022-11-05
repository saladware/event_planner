from sqlalchemy import Column, String, Integer

from ...db import Base


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    telegram_id = Column(Integer)
    hashed_password = Column(String)
