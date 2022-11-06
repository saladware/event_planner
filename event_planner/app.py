from fastapi import FastAPI
from .db import Base, engine
from .events import event_router
from .users import user_router


app = FastAPI()

app.include_router(event_router)
app.include_router(user_router)

Base.metadata.create_all(engine)
