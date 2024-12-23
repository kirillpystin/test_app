import asyncio

from fastapi import FastAPI

from app.handlers.store_handlers import (cleanup_expired_items,
                                         load_store_from_file)
from app.urls import api_router

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def startup_event() -> None:
    await load_store_from_file()
    asyncio.create_task(cleanup_expired_items())
