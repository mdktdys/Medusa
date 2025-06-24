from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import Timing
from sqlalchemy import Result, select


async def get_timings(session: AsyncSession) -> list[Timing]:
    result: Result[Tuple[database.Timings]] = await session.execute(select(database.Timings))
    return list(result.scalars().all())
