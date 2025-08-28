from typing import Optional

from fastapi import APIRouter, Depends

from src.alchemy.database_local import User
from src.alchemy.db_helper import AsyncSession, local_db_helper
from src.auth.auth import current_active_user

from . import crud
from .schemas import UserResponse

router = APIRouter(tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    response_model_exclude_none=True
)
async def get_me(user: User = Depends(current_active_user)) -> UserResponse:
    return crud.me(user=user)


@router.get("/telegram", response_model = Optional[UserResponse])
async def get_telegram_user(user_id: int, session: AsyncSession = Depends(local_db_helper.session_dependency)) -> Optional[UserResponse]:
    return await crud.get_telegram_user(user_id = user_id, session = session)