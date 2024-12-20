from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest

metrics_router = APIRouter(tags=["API для работы с метриками"])


@metrics_router.get("/metrics", summary="Метрики")
async def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")
