from typing import Optional

from fastapi import APIRouter, Depends
from src.auth.auth import current_active_user
from src.alchemy.database import User
from . import crud 
from .schemas import UserResponse

router = APIRouter(tags=["Users"])


@router.get("/me", response_model = Optional[UserResponse])
async def get_me(user: User = Depends(current_active_user)) -> UserResponse:
    return crud.me(user = user)