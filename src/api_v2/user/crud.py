import base64
from typing import Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy import Result, select

from src.alchemy.database_local import User
from src.alchemy.db_helper import AsyncSession

from .schemas import UserResponse


def me(user: User) -> UserResponse:
    photo_base64: Optional[str] = None
    if user.photo_url is not None:
        photo_base64 = base64.b64encode(user.photo_url).decode("utf-8")

    return UserResponse(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        role=user.role,
        photo_base64 = photo_base64
    )


async def get_telegram_user(user_id: int, session: AsyncSession) -> Optional[UserResponse]:
    user_result: Result[Tuple[User]] = await session.execute(select(User).where(User.telegram_id == str(user_id)))
    user: User | None = user_result.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'User not found'
        )
    
    return me(user)