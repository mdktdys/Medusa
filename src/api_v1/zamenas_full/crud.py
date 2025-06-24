from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import ZamenasFull, ZamenasFullFilter
from sqlalchemy import Result, Select, select, and_


async def get_zamenas_full(session: AsyncSession, filter: ZamenasFullFilter) -> list[ZamenasFull]:
    query: Select[Tuple[database.ZamenasFull]] = select(database.ZamenasFull)
    filters: list = []

    if filter.group:
        if isinstance(filter.group, list):
            filters.append(database.ZamenasFull.group.in_(filter.group))
        else:
            filters.append(database.ZamenasFull.group == filter.group)

    if filter.start_date:
        filters.append(database.ZamenasFull.date >= filter.start_date)
    if filter.end_date:
        filters.append(database.ZamenasFull.date <= filter.end_date)
    if filter.id:
        filters.append(database.ZamenasFull.id == filter.id)

    if filters:
        query = query.where(and_(*filters))

    result: Result[Tuple[database.ZamenasFull]] = await session.execute(query)
    return list(result.scalars().all())
