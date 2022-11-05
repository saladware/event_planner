from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import schemas, models
from ...db import get_db

oauth_scheme = OAuth2PasswordBearer('/user/token')

user_router = APIRouter(prefix='/user', tags=['user'])


def hash_password(password: str):
    return password + "aboba"


def get_user(db: Session, username) -> models.User | None:
    user = db.query(models.User).get(username)
    if user is not None:
        return schemas.User.from_orm(user)


def decode_token(token: str):
    user = get_user(next(get_db()), token)
    return user


def get_current_user(token: str = Depends(oauth_scheme)):
    user = decode_token(token)
    if user is None:
        raise HTTPException(401, 'slish, pochemu ne avtorizovan???', headers={
            'WWW-Authenticate': 'Bearer'
        })
    return user


@user_router.get("/")
async def show_me(current_user: schemas.BaseUser = Depends(get_current_user)):
    return current_user


@user_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).get(form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.User.from_orm(user)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@user_router.post('/', response_model=schemas.User)
async def create_user(user_data: schemas.CreateUser, db: Session = Depends(get_db)):
    if db.query(models.User).get(user_data.username) is not None:
        raise HTTPException(403, 'Is already exists')
    user = models.User(**user_data.dict(exclude={'password'}), hashed_password=hash_password(user_data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
