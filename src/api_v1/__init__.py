from fastapi import APIRouter
from .groups.views import router as groups_router
from .search.views import router as search_router
from .teachers.views import router as teachers_router
from .merges.views import router as merges_router
from .bench.views import router as bench_router
from .cabinets.views import router as cabinets_router
from .parser.views import router as parser_router
from .manage.views import router as manage_router
from .telegram.views import router as telegram_router

router = APIRouter()
router.include_router(router=groups_router, prefix="/groups")
router.include_router(router=search_router, prefix="/search")
router.include_router(router=teachers_router, prefix="/teachers")
router.include_router(router=merges_router, prefix="/merge")
router.include_router(router=bench_router, prefix="/bench")
router.include_router(router=cabinets_router, prefix="/cabinets")
router.include_router(router=parser_router, prefix="/parser")
router.include_router(router=manage_router, prefix="/manage")
router.include_router(router=telegram_router, prefix="/telegram")
