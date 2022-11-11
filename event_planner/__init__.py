import asyncio


from .app import app
from .bot import run


@app.on_event("startup")
async def startup_event():
    run(asyncio.get_running_loop())

