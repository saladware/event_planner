from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class CreateUser(BaseUser):
    password: str


class User(BaseUser):
    telegram_id: int
    hashed_password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
