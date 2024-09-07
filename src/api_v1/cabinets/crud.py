from typing import List
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database


async def get_cabinets(session: AsyncSession) -> List[database.Cabinets]:
    query = select(database.Cabinets)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_cabinet_by_id(
    session: AsyncSession, cabinet_id: int
) -> List[database.Cabinets]:
    query = select(database.Cabinets).where(database.Cabinets.id == cabinet_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())
