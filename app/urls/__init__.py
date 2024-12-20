from fastapi import APIRouter

from .health import health_router
from .metrics import metrics_router
from .objects import objects_router

api_router = APIRouter()
api_router.include_router(objects_router)
api_router.include_router(metrics_router)
api_router.include_router(health_router)
