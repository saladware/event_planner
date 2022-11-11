from sqlalchemy import Column, String, BigInteger

from event_planner.db import Base


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    telegram_id = Column(BigInteger, default=0)  # 0 if not verified
    hashed_password = Column(String)

    def __repr__(self):
        return f'User({self.username=}, {self.telegram_id}'

    def is_verified(self):
        return self.telegram_id != 0

    def verify(self, telegram_id: int):
        self.telegram_id = telegram_id
