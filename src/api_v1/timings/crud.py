from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import Timing
from sqlalchemy import select


async def get_timings(session: AsyncSession) -> list[Timing]:
    result: list[database.Timings] = list((await session.execute(select(database.Timings))).scalars().all())
    return result
