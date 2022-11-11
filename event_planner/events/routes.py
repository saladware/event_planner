import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from ..db import get_db
from ..users import User, get_current_user

event_router = APIRouter(prefix='/event', tags=['event'])


@event_router.get('/{event_date: date}', response_model=schemas.EventList)
def get_event_by_date(event_date: datetime.date, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    get events that are scheduled on the passed day,
    the previous day, and the next day (to be independent of the time zone)
    """

    events: models.Event = db.query(models.Event).filter(
        models.Event.planned_at.between(
            event_date - datetime.timedelta(days=1),
            event_date + datetime.timedelta(days=1),
        ),
        models.Event.author_id == user.username
    )
    return schemas.EventList(events=list(events))


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
    if event_src.planned_at <= datetime.datetime.utcnow() + datetime.timedelta(hours=2):
        raise HTTPException(404, 'Event cannot be scheduled 2 hours before it starts')
    if event_src.remind_at is None:
        event_src.remind_at = event_src.planned_at - datetime.timedelta(hours=2)
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


@event_router.delete('/{event_id: int}')
def delete_event_by_id(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event: models.Event = db.query(models.Event).get(event_id)
    if event is None:
        raise HTTPException(404, 'Event not found')
    if event.author_id != user.username:
        raise HTTPException(403, 'You are not author')
    db.delete(event)
    db.commit()
    return {'detail': 'success'}


@event_router.get('/my', response_model=schemas.EventList)
def get_my_events(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    events = db.query(models.Event).filter(models.Event.author_id == user.username)
    return schemas.EventList(events=list(events))
