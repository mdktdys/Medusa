from fastapi import APIRouter
from src.api_v1 import router as api_v1_router
from src.auth.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(api_v1_router, prefix="/api/v1")
