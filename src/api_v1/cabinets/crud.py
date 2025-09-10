import re
from typing import List, Tuple

from sqlalchemy import Result, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database_local


async def get_cabinets(session: AsyncSession) -> List[database_local.Cabinet]:
    query: Select[Tuple[database_local.Cabinet]] = select(database_local.Cabinet)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_cabinet_by_id(
    session: AsyncSession, cabinet_id: int
) -> List[database_local.Cabinet]:
    query = select(database_local.Cabinet).where(database_local.Cabinet.id == cabinet_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_cabinets_normalized_contains(session: AsyncSession, raw_name: str) -> list[database_local.Cabinet]:
    normalized: str = re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', raw_name).lower()
    query: Select[Tuple[database_local.Cabinet]] = (
        select(database_local.Cabinet)
        .where(
            func.lower(
                func.regexp_replace(database_local.Group.name, r'[^a-zA-Zа-яА-Я0-9]', '', 'g')
            ).like(f"%{normalized}%")
        )
    )

    result: Result = await session.execute(query)
    return list(result.scalars().all())