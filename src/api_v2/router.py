from fastapi import APIRouter
from .client.data.views import router as data_router
from .client.zamena.views import router as zamena_router

router = APIRouter()

# public
router.include_router(data_router, prefix="/data")
router.include_router(zamena_router, prefix="/zamena")