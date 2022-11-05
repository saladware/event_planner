from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from ..db import get_db
from ..users import User, get_current_user


event_router = APIRouter(prefix='/event', tags=['event'])


@event_router.get('/{event_id: int}', response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event: models.Event = db.query(models.Event).get(event_id)
    if event is None:
        raise HTTPException(404, 'Not found')
    if event.author_id != user.username:
        raise HTTPException(403, 'you are not author')
    return event


@event_router.get('/my')
def get_my_events(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    events = db.query(models.Event).filter(models.Event.author_id == user.username)
    return list(events)


@event_router.post('/', response_model=schemas.Event)
def create_event(event_src: schemas.CreateEvent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = models.Event(**event_src.dict(), author_id=user.username)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
