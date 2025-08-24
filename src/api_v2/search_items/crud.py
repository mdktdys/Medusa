from typing import List, Tuple

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.database_local import SearchItem


async def get_seach_items(session: AsyncSession) -> List[SearchItem]:
    result: Result[Tuple[SearchItem]] = await session.execute(select(SearchItem))
    return list(result.scalars().all())