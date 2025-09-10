from typing import List, Tuple, Union

from sqlalchemy import Result, Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database_local

from .schemas import Lesson, LessonFilter


async def get_lessons(session: AsyncSession, filter: LessonFilter):
    query: Select[Tuple[database_local.Lesson]] = select(database_local.Lesson)

    filters: list = []

    if filter.group:
        if isinstance(filter.group, list):
            filters.append(database_local.Lesson.group_id.in_(filter.group))
        else:
            filters.append(database_local.Lesson.group_id == filter.group)

    if filter.start_date:
        filters.append(database_local.Lesson.date_ >= filter.start_date)
    if filter.end_date:
        filters.append(database_local.Lesson.date_ <= filter.end_date)
    if filter.number:
        filters.append(database_local.Lesson.timing_id == filter.number)
    if filter.course:
        filters.append(database_local.Lesson.discipline_id == filter.course)
    if filter.teacher:
        filters.append(database_local.Lesson.teacher_id == filter.teacher)
    if filter.cabinet:
        filters.append(database_local.Lesson.cabinet == filter.cabinet)
    if filter.id:
        filters.append(database_local.Lesson.id == filter.id)

    if filters:
        query = query.where(and_(*filters))

    result: Result[Tuple[database_local.Lesson]] = await session.execute(query)
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