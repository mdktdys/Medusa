from sqlalchemy.engine import Result
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import Group


async def get_search_items(session: AsyncSession, search_filter: str):
    query = select(Group).where(Group.name.icontains(search_filter))
    result: Result = await session.execute(query)
    groups = list(result.scalars().all())
    return groups
