from fastapi import APIRouter
from .groups.views import router as groups_router
from .search.views import router as search_router
from .teachers.views import router as teachers_router
from .merges.views import router as merges_router

router = APIRouter()
router.include_router(router=groups_router, prefix="/groups")
router.include_router(router=search_router, prefix="/search")
router.include_router(router=teachers_router, prefix="/teachers")
router.include_router(router=merges_router, prefix="/merge")
