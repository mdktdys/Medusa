import uuid
from typing import Tuple

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database

from .schemas import AuthStatusDto, CreateStateDto


async def create_state(session: AsyncSession) -> CreateStateDto:
    token: str = str(uuid.uuid4())
    session.add(database.TelegramAuthState(token = token))
    await session.commit()
    return CreateStateDto(token = token)


async def auth_status(token: str, session: AsyncSession) -> AuthStatusDto | None:
    result: Result[Tuple[database.TelegramAuthState]] = await session.execute(select(database.TelegramAuthState).where(database.TelegramAuthState.token == token))
    state: database.TelegramAuthState | None = result.scalars().first()

    if state is None:
        return None

    await session.delete(state)
    await session.commit()
    return AuthStatusDto(
        access_token = state.access_token,
        refresh_token = state.refresh_token
    )