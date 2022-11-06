from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from ..db import get_db
from ..users import User, get_current_user

event_router = APIRouter(prefix='/event', tags=['event'])


@event_router.get('/{event_id: int}', response_model=schemas.Event)
def get_event_by_id(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event: models.Event = db.query(models.Event).get(event_id)
    if event is None:
        raise HTTPException(404, 'Event not found')
    if event.author_id != user.username:
        raise HTTPException(403, 'you are not author')
    return event


@event_router.post('/', response_model=schemas.Event)
def create_event(event_src: schemas.CreateEvent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = models.Event(**event_src.dict(), author_id=user.username)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@event_router.put('/{event_id: int}', response_model=schemas.Event)
def change_event_by_id(event_id: int, data: schemas.UpdateEvent, db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    event: models.Event = db.query(models.Event).get(event_id)
    if event is None:
        raise HTTPException(404, 'Event not found')
    if event.author_id != user.username:
        raise HTTPException(403, 'you are not author')
    for key, value in data.dict().items():
        if getattr(event, key) != value and value:
            setattr(event, key, value)
    db.commit()
    return event


@event_router.delete('/{event_id: int}', response_model=schemas.Event)
def delete_event_by_id(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event: models.Event = db.query(models.Event).get(event_id)
    if event is None:
        raise HTTPException(404, 'Event not found')
    if event.author_id != user.username:
        raise HTTPException(403, 'you are not author')
    db.delete(event)
    db.commit()
    return {'detail': 'success'}


@event_router.get('/my')
def get_my_events(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    events = db.query(models.Event).filter(models.Event.author_id == user.username)
    return list(events)
