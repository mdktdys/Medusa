from typing import List, Tuple, Union

from sqlalchemy import Result, Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database, database_local

from .schemas import Lesson, LessonFilter


async def get_lessons(session: AsyncSession, filter: LessonFilter) -> list[Lesson]:
    query: Select[Tuple[database.Paras]] = select(database.Paras)

    filters: list = []

    if filter.group:
        if isinstance(filter.group, list):
            filters.append(database.Paras.group.in_(filter.group))
        else:
            filters.append(database.Paras.group == filter.group)

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


async def create_lessons(session: AsyncSession, request: Union[Lesson, List[Lesson]]):
    lessons_data: List[Lesson] = [request] if isinstance(request, Lesson) else request

    lessons = []
    for item in lessons_data:
        lesson = database_local.Lesson(
            date_ = item.date,
            timing_id = item.number,
            teacher_id = item.teacher_id,
            discipline_id = item.discipline_id,
            cabinet_id = item.cabinet_id,
            group_id = item.group_id,
        )
        session.add(lesson)
        lessons.append(lesson)

    await session.commit()
    return {"result": "ok", "count": len(lessons)}