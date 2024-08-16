"""
Read
"""

from sqlalchemy.engine import Result
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import Group


async def get_groups(session: AsyncSession) -> list[Group]:
    query = select(Group)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_by_id(session: AsyncSession, group_id: int) -> list[Group]:
    query = select(Group).where(Group.id.in_([group_id]))
    result: Result = await session.execute(query)
    return list(result.scalars().all())
