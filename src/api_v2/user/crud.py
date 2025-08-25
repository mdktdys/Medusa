import base64
from typing import Tuple

from sqlalchemy import Result, select

from src.alchemy.database import User
from src.alchemy.db_helper import AsyncSession

from .schemas import UserResponse


def me(user: User) -> UserResponse:
    photo_base64 = None
    if user.photo_url:
        photo_base64: str = base64.b64encode(user.photo_url).decode("utf-8")

    return UserResponse(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        role=user.role,
        photo_base64=photo_base64
    )



async def get_telegram_user(user_id: int, session: AsyncSession) -> UserResponse:
    user: Result[Tuple[User]] = await session.execute(select(User).where(User.telegram_id == str(user_id)))
    return me(user.scalars().first())