from typing import List
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from src.alchemy import database
from src.api_v1.search.schemas import SearchResult


async def get_search_items(
    session: AsyncSession, search_filter: str
) -> List[SearchResult]:
    async def search_groups():
        query = select(database.Groups).where(
            database.Groups.name.icontains(search_filter)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    async def search_teachers():
        query = select(database.Teachers).where(
            database.Teachers.name.icontains(search_filter)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    # Запускаем оба запроса параллельно
    groups_task, teachers_task = await asyncio.gather(
        search_groups(), search_teachers()
    )

    groups = groups_task
    teachers = teachers_task

    # Объединяем результаты поиска групп и преподавателей
    search_results = groups + teachers

    # Создаем список SearchResult с использованием спискового включения
    res = [
        SearchResult(
            search_type="group" if isinstance(i, database.Groups) else "teacher",
            search_id=i.id,
            search_name=i.name,
            search_image="https://abtechsolutions.ca/wp-content/uploads/2019/02/Test.png",
        )
        for i in search_results
    ]

    return res
