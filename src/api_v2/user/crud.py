from typing import Tuple
from src.alchemy.db_helper import AsyncSession
from src.alchemy.database import User
from sqlalchemy import Result, select
from .schemas import UserResponse

def me(user: User) -> UserResponse:
    return UserResponse(
        email = user.email,
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        role = user.role
    )


async def get_telegram_user(user_id: int, session: AsyncSession) -> UserResponse:
    user: Result[Tuple[User]] = await session.execute(select(User).where(User.telegram_id == str(user_id)))
    return me(user.first())