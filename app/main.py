import asyncio

import uvloop

from app.create_app import create_app

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = create_app()
