from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import schemas, models
from .auth import hash_password, get_current_user, create_access_token, authenticate_user
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..db import get_db
from ..bot import get_link

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.get("/")
async def show_me(current_user: schemas.BaseUser = Depends(get_current_user)):
    return current_user


@user_router.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        url = await get_link()
        raise HTTPException(
            status_code=401,
            detail=f"Incorrect username or password. Maybe user not verified. Pls register user and verify it at {url}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post('/', response_model=schemas.User)
async def register_user(user_data: schemas.CreateUser, db: Session = Depends(get_db)):
    if db.query(models.User).get(user_data.username) is not None:
        raise HTTPException(403, 'Is already exists')
    user = models.User(**user_data.dict(exclude={'password'}), hashed_password=hash_password(user_data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
