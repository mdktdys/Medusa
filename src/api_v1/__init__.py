from fastapi import APIRouter, Depends

from src.auth.auth import any_auth_method

from .already_found_links.views import router as already_found_links_router
from .bench.views import router as bench_router
from .cabinets.views import router as cabinets_router
from .courses.views import router as courses_router
from .departments.views import router as departments_router
from .groups.views import router as groups_router
from .lessons.views import router as lessons_router
from .manage.views import router as manage_router
from .merges.views import router as merges_router
from .notifications.views import router as notifications_router
from .parser.views import router as parser_router
from .search.views import router as search_router
from .teachers.views import router as teachers_router
from .telegram.views import router as telegram_router
from .timings.views import router as timings_router
from .zamena_file_links.views import router as zamena_file_links_router
from .zamenas.views import router as zamenas_router
from .zamenas_full.views import router as zamenas_full_router

router = APIRouter()

# Public
router.include_router(router = groups_router, prefix="/groups")
router.include_router(router = teachers_router, prefix="/teachers")
router.include_router(router = cabinets_router, prefix="/cabinets")
router.include_router(router = departments_router, prefix='/departments')
router.include_router(router = courses_router, prefix = '/courses')
router.include_router(router = lessons_router, prefix = '/lessons')
router.include_router(router = zamenas_router, prefix = '/zamenas')
router.include_router(router = zamenas_full_router, prefix = '/zamenas_full')
router.include_router(router = timings_router, prefix = '/timings')
router.include_router(router = already_found_links_router, prefix = '/already_found_links')
router.include_router(router = zamena_file_links_router, prefix = '/zamena_file_links')

# Private
router.include_router(router = search_router, prefix="/search", dependencies=[Depends(any_auth_method(roles=["Owner"]))])
router.include_router(router = merges_router, prefix="/merge", dependencies=[Depends(any_auth_method(roles=["Owner"]))])
router.include_router(router = bench_router, prefix="/bench", dependencies=[Depends(any_auth_method(roles=["Owner"]))])
router.include_router(router = parser_router, prefix="/parser", dependencies=[Depends(any_auth_method(roles=["Owner"]))])
router.include_router(router = manage_router, prefix="/manage", dependencies=[Depends(any_auth_method(roles=["Owner"]))])
router.include_router(router = telegram_router, prefix="/telegram", dependencies=[Depends(any_auth_method(roles=["Owner"]))])
router.include_router(router = notifications_router, prefix="/notifications", dependencies=[Depends(any_auth_method(roles=["Owner"]))])