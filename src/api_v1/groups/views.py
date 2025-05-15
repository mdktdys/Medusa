from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud
from .schemas import Group, DayScheduleFormatted
from .schemas import DaySchedule

router = APIRouter(tags=["Groups"])


@router.get("/", response_model = list[Group])
@cache(expire=6000)
async def get_groups(session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Group]:
    return await crud.get_groups(session=session)


@router.get("/id/{group_id}/", response_model=list[Group])
@cache(expire=6000)
async def get_group_by_id(group_id: int = -1, session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Group]:
    return await crud.get_group_by_id(session=session, group_id=group_id)


@router.get("/day_schedule/{group_id}/{date}/{chat_id}/", response_model=DaySchedule)
@cache(expire=6000)
async def get_group_day_schedule_by_date(
    group_id: int = -1,
    chat_id: int = -1,
    date: datetime = datetime.now(),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> DaySchedule:
    return await crud.get_group_day_schedule_by_date(session=session, group_id=group_id, date=date)


@router.get("/day_schedule_formatted/{group_id}/{date}/{chat_id}/", response_model=DayScheduleFormatted)
async def get_group_day_schedule_by_date_formatted(
    group_id: int = -1,
    chat_id: int = -1,
    date: datetime = datetime.now(),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> DayScheduleFormatted:
    return await crud.get_group_day_schedule_by_date_formatted(session=session, group_id=group_id, date=date, chat_id=chat_id)


@router.get("/week_schedule/{group_id}/{monday_date}/", response_model=List[DaySchedule])
@cache(expire=6000)
async def get_group_week_schedule_by_date(
    group_id: int = -1,
    monday_date: datetime = datetime.now(),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[DaySchedule]:
    return await crud.get_group_week_schedule_by_date(
        monday_date=monday_date,
        group_id=group_id,
        session=session,
    )