from fastapi import APIRouter

from .log.router import router as log_router
from .about.router import router as about_router

router = APIRouter()

router.include_router(log_router)
router.include_router(about_router)
