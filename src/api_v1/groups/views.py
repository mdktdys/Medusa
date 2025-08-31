from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import AsyncSession, db_helper
from src.auth.auth import any_auth_method
from src.data.data_source import DataSource
from src.dependencies.data_source_dependency import get_supabase_data_source
from src.utils.ai_requests import send_ai_request

from . import crud
from .schemas import (CreateGroupRequest, DaySchedule, DayScheduleFormatted,
                      Group, GroupScheduleRequest, GroupScheduleResponse)

namespace: str = 'Groups'
router = APIRouter(tags=[namespace])


@router.get('/pretty', response_class = PlainTextResponse)
def get_pretty():
    prompt = 'Напиши моей девушке подбадривающий компимент чтобы она не унывала, будь оригинальным и не пищи банальщину, сообщение должно быть коротким буквально в 1 предложение. Пиши как реальный человек не используй клеше'
    result = send_ai_request(request = prompt)
    print(result)
    return result


@router.get("/", response_model = list[Group])
@cache(expire = 6000, namespace = namespace)
async def get_groups(session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Group]:
    return await crud.get_groups(session=session)


@router.get("/id/{group_id}/", response_model=list[Group])
@cache(expire = 6000, namespace = namespace)
async def get_group_by_id(group_id: int = -1, session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Group]:
    return await crud.get_group_by_id(session=session, group_id=group_id)


@router.put("/{group_id}", response_model = Group, dependencies = [Depends(any_auth_method(roles=["Owner"]))])
async def update_group(
    group_id: int,
    data: Group,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Group:
    result: Group = await crud.update_group(session, group_id, data)
    await FastAPICache.clear(namespace = namespace)
    return result


@router.delete("/{group_id}", dependencies = [Depends(any_auth_method(roles=["Owner"]))])
async def delete_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict[str, str]:
    result: dict[str, str] = await crud.delete_group(session, group_id)
    await FastAPICache.clear(namespace = namespace)
    return result


@router.post("/", response_model = Group, status_code=201, dependencies = [Depends(any_auth_method(roles=["Owner"]))])
async def create_group(
    request: CreateGroupRequest,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Group:
    result: Group = await crud.create_group(session=session, data = request)
    # await FastAPICache.clear(namespace = namespace)
    return result


# Schedule
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
    

@router.post('/schedule', response_model = GroupScheduleResponse)
@cache(expire = 60000)
async def get_group_schedule(
    request: GroupScheduleRequest,
    datasource: DataSource = Depends(get_supabase_data_source)
) -> GroupScheduleResponse:
    return await crud.get_group_schedule(
        request = request,
        datasource = datasource,
    )