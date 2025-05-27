from typing import List, Tuple
from sqlalchemy.engine import Result
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from src.alchemy import database
from src.api_v1.search.schemas import SearchResult


async def get_search_items(
    session: AsyncSession, search_filter: str
) -> List[SearchResult]:

    async def search_groups():
        query: Select[Tuple[database.Groups]] = select(database.Groups).where(
            database.Groups.name.icontains(search_filter)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    async def search_teachers():
        query: Select[Tuple[database.Teachers]] = select(database.Teachers).where(
            database.Teachers.name.icontains(search_filter)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    groups_task, teachers_task = await asyncio.gather(
        search_teachers(),
        search_groups(),
    )

    groups = groups_task
    teachers = teachers_task
    search_results = groups + teachers

    res: List[SearchResult] = [
        SearchResult(
            search_type= "group" if isinstance(i, database.Groups) else "teacher",
            search_image = i.image if i.image is not None else '',
            search_name = i.name,
            search_id = i.id,
        )
        for i in search_results
    ]

    return res
