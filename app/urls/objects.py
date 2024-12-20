from fastapi import APIRouter

from app.handlers.object_handlers import create_item, get_item
from app.schemas.object_schema import ObjectBody

objects_router = APIRouter(tags=["API для работы с объектами"])


@objects_router.put(
    path="/objects/{key}",
    summary="Запись объектов в хранилище",
)
async def add_object(body: ObjectBody, key) -> dict:
    return await create_item(key, body)


@objects_router.get(
    path="/objects/{key}",
    summary="Получение объектов из хранилища",
)
async def get_object(key: str) -> dict:
    return await get_item(key)
