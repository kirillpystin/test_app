import json

from fastapi import APIRouter, HTTPException
from starlette import status

from app.configs.storage import file_path

health_router = APIRouter(tags=["API для работы с состоянием сервиса"])


@health_router.get("/health/liveness", summary="Проверка работоспособности")
async def liveness() -> dict[str, str]:
    return {"status": "alive"}


@health_router.get("/health/readiness", summary="Проверка готовности")
async def readiness() -> dict[str, str]:
    try:
        with open(file_path, "r") as f:
            json.load(f)
        return {"status": "ready"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="not ready"
        )
