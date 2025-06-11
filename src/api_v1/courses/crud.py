from typing import Tuple

from sqlalchemy import Select, select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import Course


async def get_courses(session: AsyncSession) -> list[Course]:
    query: Select[Tuple[database.Courses]] = select(database.Courses)
    result: Result = await session.execute(query)
    return list(result.scalars().all())