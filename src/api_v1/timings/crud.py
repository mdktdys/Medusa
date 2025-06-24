from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import Timing
from sqlalchemy import select


async def get_timings(session: AsyncSession) -> list[Timing]:
    result: list[database.Timings] = list((await session.execute(select(database.Timings))).scalars().all())
    
    timings: list[Timing] = []
    for time in result:
        timing = Timing(
            number = time.number,
            start = time.start,
            end = time.end,
            saturday_start = time.saturdayStart,
            saturday_end = time.saturdayEnd,
            obed_end = time.obedEnd,
            obed_start = time.obedStart,
        )
        timings.append(timing)
    
    return timings
