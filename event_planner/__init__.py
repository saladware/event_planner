from fastapi import FastAPI
from .db import Base, engine
from .apps.events import event_router

app = FastAPI()

app.include_router(event_router)

Base.metadata.create_all(engine)
