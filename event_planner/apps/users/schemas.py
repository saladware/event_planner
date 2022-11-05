from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    telegram_id: int


class CreateUser(BaseUser):
    password: str


class User(BaseUser):
    hashed_password: str

    class Config:
        orm_mode = True
