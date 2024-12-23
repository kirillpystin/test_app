import time

from fastapi import HTTPException

from app.configs.metrics import active_items, items_stored
from app.configs.storage import store, store_lock
from app.handlers.store_handlers import save_store_to_file
from app.schemas.object_schema import ObjectBody


async def create_item(key: str, item: ObjectBody) -> dict[str, str]:
    expiration = time.time() + item.expires if item.expires else None
    async with store_lock:
        store[key] = {"value": item.data, "expiration": expiration}
        items_stored.inc()
        active_items.set(len(store))
        await save_store_to_file()
    return {"message": "Item stored successfully."}


async def get_item(key: str) -> dict:
    async with store_lock:
        item = store.get(key)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if item["expiration"] and item["expiration"] < time.time():
            del store[key]
            active_items.set(len(store))
            await save_store_to_file()
            raise HTTPException(status_code=404, detail="Item expired")
        return item["value"]
