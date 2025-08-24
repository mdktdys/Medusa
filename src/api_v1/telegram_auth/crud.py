import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database

from .schemas import CreateStateDto


async def create_state(session: AsyncSession) -> CreateStateDto:
    token: str = str(uuid.uuid4())
    session.add(database.TelegramAuthState(token = token))
    await session.commit()
    return CreateStateDto(token = token)
