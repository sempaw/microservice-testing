from fastapi import APIRouter

from .routers import contract, spec

router = APIRouter(
    prefix="/v1",
)

router.include_router(contract.router)
router.include_router(spec.router)
