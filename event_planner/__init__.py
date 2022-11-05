"""
TODO: migrations
TODO: telegram integration
TODO: run application in docker with uvloop
"""

from fastapi import FastAPI
from .db import Base, engine
from event_planner.events import event_router
from event_planner.users import user_router


app = FastAPI()

app.include_router(event_router)
app.include_router(user_router)

Base.metadata.create_all(engine)
