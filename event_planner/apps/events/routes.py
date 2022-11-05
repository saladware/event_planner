from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...db import get_db
from . import scheams, models
from ..users import User, get_current_user

event_router = APIRouter(prefix='/event', tags=['event'])


@event_router.get('/{event_id}')
def get_event(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = db.query(models.Event).get(event_id)
    return event


@event_router.post('/', response_model=scheams.Event)
def create_event(event_src: scheams.CreateEvent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = models.Event(**event_src.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
