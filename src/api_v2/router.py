from fastapi import APIRouter
from .client.data.views import router as data_router
from .client.zamena.views import router as zamena_router
from .user.views import router as user_router
from fastapi import Depends

from src.auth.auth import any_auth_method

router = APIRouter()

# public
router.include_router(data_router, prefix="/data")
router.include_router(zamena_router, prefix="/zamena")

# private
router.include_router(user_router, prefix="/users", dependencies=[Depends(any_auth_method(roles=['Owner', 'Guest']))])