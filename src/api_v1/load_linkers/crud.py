from typing import Tuple

from sqlalchemy import Delete, Result, Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database_local

from .schemas import (CreateLoadLinkRequest, DeleteLoadLinkRequest,
                      LoadLinkersRequest)


async def get_load_linkers(session: AsyncSession, request: LoadLinkersRequest):
    query: Select[Tuple[database_local.LoadLink]] = select(database_local.LoadLink).where(database_local.LoadLink.group_id == request.group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def create_load_link(session: AsyncSession, request: CreateLoadLinkRequest):
    new_link = database_local.LoadLink(
        first_year_hours = request.first_year_hours,
        second_year_hours = request.second_year_hours,
        teacher_id = request.teacher_id,
        discipline_code_id = request.discipline_code_id,
        group_id = request.group_id,
        discipline_id = request.discipline_id,
    )
    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)
    return new_link


async def delete_load_link(session: AsyncSession, request: DeleteLoadLinkRequest):
    query: Delete = delete(database_local.LoadLink).where(database_local.LoadLink.id == request.id)
    await session.execute(query)
    await session.commit()
    return {"status": "ok"}