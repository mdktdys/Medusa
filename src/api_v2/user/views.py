from typing import Optional
from src.alchemy.db_helper import AsyncSession, db_helper
from fastapi import APIRouter, Depends
from src.auth.auth import current_active_user
from src.alchemy.database import User
from . import crud 
from .schemas import UserResponse


router = APIRouter(tags=["Users"])


@router.get("/me", response_model = Optional[UserResponse])
async def get_me(user: User = Depends(current_active_user)) -> UserResponse:
    return crud.me(user = user)


@router.get("/telegram", response_model = Optional[UserResponse])
async def get_telegram_user(user_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> UserResponse:
    return await crud.get_telegram_user(user_id = user_id, session = session)