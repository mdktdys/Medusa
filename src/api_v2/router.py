from fastapi import APIRouter, Depends

from src.auth.auth import any_auth_method

from .client.data.views import router as data_router
from .client.zamena.views import router as zamena_router
from .search_items.views import router as search_items_router
from .user.views import router as user_router

router = APIRouter()

# public
router.include_router(data_router, prefix = '/data')
router.include_router(zamena_router, prefix = '/zamena')
router.include_router(search_items_router, prefix = '/search_items')

# private
router.include_router(user_router, prefix="/users", dependencies=[Depends(any_auth_method(roles=['Owner', 'Guest']))])
