from typing import Tuple

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database_local

from .schemas import LoadLinkersRequest


async def get_load_linkers(session: AsyncSession, request: LoadLinkersRequest):
    query: Select[Tuple[database_local.LoadLink]] = select(database_local.LoadLink).where(database_local.Group.id == request.group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())