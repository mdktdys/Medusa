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

    groups_task, teachers_task = await asyncio.gather(
        search_groups(), search_teachers()
    )

    groups = groups_task
    teachers = teachers_task
    search_results = groups + teachers

    res = [
        SearchResult(
            search_type="group" if isinstance(i, database.Groups) else "teacher",
            search_id=i.id,
            search_name=i.name,
            search_image="https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/python_(1).png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL3B5dGhvbl8oMSkucG5nIiwiaWF0IjoxNzM4NTMzMDQ0LCJleHAiOjE3NzAwNjkwNDR9.C1p9_bssrMmsqQEd203gQLhBb1MLYC5CfaxMqbMIFCU",
        )
        for i in search_results
    ]

    return res
