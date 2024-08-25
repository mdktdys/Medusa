from sqlalchemy.engine import Result
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database


async def get_search_items(session: AsyncSession, search_filter: str):
    query = select(database.Groups).where(database.Groups.name.icontains(search_filter))
    result: Result = await session.execute(query)
    groups = list(result.scalars().all())
    return groups
