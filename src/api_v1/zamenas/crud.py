from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import Zamena, ZamenaFilter
from sqlalchemy import Result, Select, select, and_


async def get_zamenas(session: AsyncSession, filter: ZamenaFilter) -> list[Zamena]:
    query: Select[Tuple[database.Zamenas]] = select(database.Zamenas)
    filters: list = []

    if filter.group:
        if isinstance(filter.group, list):
            filters.append(database.Zamenas.group.in_(filter.group))
        else:
            filters.append(database.Zamenas.group == filter.group)

    if filter.start_date:
        filters.append(database.Zamenas.date >= filter.start_date)
    if filter.end_date:
        filters.append(database.Zamenas.date <= filter.end_date)
    if filter.number:
        filters.append(database.Zamenas.number == filter.number)
    if filter.course:
        filters.append(database.Zamenas.course == filter.course)
    if filter.teacher:
        filters.append(database.Zamenas.teacher == filter.teacher)
    if filter.cabinet:
        filters.append(database.Zamenas.cabinet == filter.cabinet)
    if filter.id:
        filters.append(database.Zamenas.id == filter.id)

    if filters:
        query = query.where(and_(*filters))

    result: Result[Tuple[database.Zamenas]] = await session.execute(query)
    return list(result.scalars().all())
