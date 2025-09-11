from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import local_db_helper
from src.auth.schemas import UserCreate, UserRead

from .auth import (
    any_auth_method,
    auth_backend,
    fastapi_users,
    get_jwt_strategy,
    get_user_manager,
)
from .schemas import TelegramWebAppRequest

router = APIRouter(tags=["Auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    dependencies=[Depends(any_auth_method(roles=["Owner"]))],
    tags=["Auth"],
)

@router.post("/telegram/webapp")
async def telegram_webapp_login(
    request: TelegramWebAppRequest,
    session: AsyncSession = Depends(local_db_helper.session_dependency),
    user_manager = Depends(get_user_manager),
    jwt_strategy = Depends(get_jwt_strategy),
):
    return {
        'result': request.user['username'],
        'raw': request.model_dump()
    }