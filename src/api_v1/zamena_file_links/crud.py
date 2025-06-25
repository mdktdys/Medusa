from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import ZamenaFileLink, ZamenaFileLinksFilter
from sqlalchemy import Result, Select, select, and_


async def get_zamena_file_links(session: AsyncSession, filter: ZamenaFileLinksFilter) -> list[ZamenaFileLink]:
    query: Select[Tuple[database.ZamenaFileLinks]] = select(database.ZamenaFileLinks)
    filters: list = []

    if filter.start_date:
        filters.append(database.ZamenaFileLinks.date >= filter.start_date)
    if filter.end_date:
        filters.append(database.ZamenaFileLinks.date <= filter.end_date)

    if filters:
        query = query.where(and_(*filters))

    result: Result[Tuple[database.ZamenaFileLinks]] = await session.execute(query)
    return list(result.scalars().all())
