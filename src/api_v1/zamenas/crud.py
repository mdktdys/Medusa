from typing import Tuple, List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database_local
from .schemas import ZamenaFilter, CreateZamenaRequest, ZamenaSwap, ZamenaGroup
from sqlalchemy import Result, Select, select, and_


async def get_zamenas(session: AsyncSession, filter: ZamenaFilter):
    query: Select[Tuple[database_local.Zamena]] = select(database_local.Zamena)
    filters: list = []

    if filter.start_date:
        filters.append(database_local.Zamena.date_ >= filter.start_date)
    if filter.end_date:
        filters.append(database_local.Zamena.date_ <= filter.end_date)
    if filter.id:
        filters.append(database_local.Zamena.id == filter.id)

    if filters:
        query = query.where(and_(*filters))

    result: Result[Tuple[database_local.Zamena]] = await session.execute(query)
    return list(result.scalars().all())


async def create_zamena(session: AsyncSession, request: CreateZamenaRequest):
    zamena = database_local.Zamena(
        date_ = request.date,
        saturday_timings = request.saturday_timings,
        file_url = request.file_url,
        file_hash = request.file_hash,
    )
    session.add(zamena)
    await session.commit()
    await session.refresh(zamena)
    return zamena



async def create_zamena_swaps(session: AsyncSession, request: List[ZamenaSwap]):
    zamena_swaps = []
    for item in request:
        zamena_swap = database_local.ZamenaSwaps(
            zamena_id = item.zamena_id,
            group_id = item.group_id,
            timing_id = item.number,
            course_id = item.course_id,
            teacher_id = item.teacher_id,
            cabinet_id = item.cabinet_id,
        )
        session.add(zamena_swap)
        zamena_swaps.append(zamena_swap)
    await session.commit()
    return {'result': 'ok', 'count': len(zamena_swaps)}



async def create_zamena_group(session: AsyncSession, request: List[ZamenaGroup]):
    zamena_groups = []
    for item in request:
        zamena_group = database_local.ZamenaGroup(
            zamena_id = item.zamena_id,
            group_id = item.group_id,
            type = item.type,
        )
        session.add(zamena_group)
        zamena_groups.append(zamena_group)
    await session.commit()
    return {'result': 'ok', 'count': len(zamena_groups)}


    