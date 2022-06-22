from fastapi import APIRouter

from .api_v1 import api_v1


router = APIRouter(
    prefix="/api",
)

router.include_router(api_v1.router)
