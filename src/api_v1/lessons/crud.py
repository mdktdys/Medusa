from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import Lesson, LessonFilter
from sqlalchemy import Result, Select, select, and_


async def get_lessons(session: AsyncSession, filter: LessonFilter) -> list[Lesson]:
    query: Select[Tuple[database.Paras]] = select(database.Paras)

    filters: list = []

    if filter.group:
        if isinstance(filter.group, list):
            filters.append(database.Zamenas.group.in_(filter.group))
        else:
            filters.append(database.Zamenas.group == filter.group)

    if filter.start_date:
        filters.append(database.Paras.date >= filter.start_date)
    if filter.end_date:
        filters.append(database.Paras.date <= filter.end_date)
    if filter.number:
        filters.append(database.Paras.number == filter.number)
    if filter.course:
        filters.append(database.Paras.course == filter.course)
    if filter.teacher:
        filters.append(database.Paras.teacher == filter.teacher)
    if filter.cabinet:
        filters.append(database.Paras.cabinet == filter.cabinet)
    if filter.id:
        filters.append(database.Paras.id == filter.id)

    if filters:
        query = query.where(and_(*filters))

    result: Result[Tuple[database.Paras]] = await session.execute(query)
    return list(result.scalars().all()) 