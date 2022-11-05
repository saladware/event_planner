from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...db import get_db
from . import schemas, models
from ..users import User, get_current_user

event_router = APIRouter(prefix='/event', tags=['event'])


@event_router.get('/{event_id}')
def get_event(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = db.query(models.Event).get(event_id)
    return event


@event_router.post('/', response_model=schemas.Event)
def create_event(event_src: schemas.CreateEvent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = models.Event(**event_src.dict(), author_id=user.username)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
