from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from .schemas import AlreadyFoundLinkFilter, AlreadyFoundLink
from sqlalchemy import Result, Select, select, and_


async def get_already_found_links(session: AsyncSession, filter: AlreadyFoundLinkFilter) -> list[AlreadyFoundLink]:
    query: Select[Tuple[database.AlreadyFoundsLinks]] = select(database.AlreadyFoundsLinks)
    filters: list = []

    if filter.start_date:
        filters.append(database.AlreadyFoundsLinks.date >= filter.start_date)
    if filter.end_date:
        filters.append(database.AlreadyFoundsLinks.date <= filter.end_date)

    if filters:
        query = query.where(and_(*filters))

    result: Result[Tuple[database.AlreadyFoundsLinks]] = await session.execute(query)
    return list(result.scalars().all())
