from fastapi import APIRouter
from .client.data.views import router as data_router

router = APIRouter()

# public
router.include_router(data_router, prefix="/data")