from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.api_v1.groups.schemas import GroupScheduleRequest, GroupScheduleResponse
from src.data.data_source import DataSource
from src.dependencies.data_source_dependency import get_supabase_data_source
from src.alchemy.database import Teachers
from src.alchemy.db_helper import db_helper, AsyncSession
from . import crud
from .schemas import (
    DayScheduleFormatted,
    Teacher,
    Queue,
    DayScheduleTeacherPydantic,
    AddQueueEntryForm,
)

router = APIRouter(tags=["Teachers"])


@router.get("/", response_model=list[Teacher])
@cache(expire=6000)
async def get_groups(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_teachers(session=session)


@router.get("/id/{teacher_id}/", response_model=list[Teacher])
@cache(expire=6000)
async def get_teacher_by_id(teacher_id: int = -1, session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Teachers]:
    return await crud.get_teacher_by_id(session=session, teacher_id=teacher_id)


@router.get("/day_schedule/{teacher_id}/{date}/{chat_id}/", response_model = DayScheduleTeacherPydantic)
@cache(expire=6000)
async def get_teacher_day_schedule_by_date(
    teacher_id: int = -1,
    date: datetime = datetime.now(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_teacher_day_schedule_by_date(session = session, teacher_id = teacher_id, date = date)


@router.get("/day_schedule_formatted/{teacher_id}/{date}/{chat_id}/", response_model=DayScheduleFormatted)
async def get_teacher_day_schedule_by_date_formatted(
    teacher_id: int = -1,
    chat_id: int = -1,
    date: datetime = datetime.now(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_teacher_day_schedule_by_date_formatted(session=session, teacher_id=teacher_id, date=date, chat_id=chat_id)


@router.get("/week_schedule/{teacher_id}/{monday_date}/", response_model=List[DayScheduleTeacherPydantic])
async def get_teacher_week_schedule_by_date(
    teacher_id: int = -1,
    monday_date: datetime = datetime.now(),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[DayScheduleTeacherPydantic]:
    return await crud.get_teacher_week_schedule_by_date(session=session, teacher_id=teacher_id, monday_date=monday_date)


@router.post('/schedule', response_model = GroupScheduleResponse)
@cache(expire = 60000)
async def get_teacher_schedule(
    request: GroupScheduleRequest,
    datasource: DataSource = Depends(get_supabase_data_source)
) -> GroupScheduleResponse:
    return await crud.get_teacher_schedule(
        request = request,
        datasource = datasource,
    )


@router.get("/queues/{teacher_id}", response_model=List[Queue])
async def get_teacher_queues(teacher_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Queue]:
    return await crud.get_teacher_queues(session = session,teacher_id = teacher_id)
    
    

@router.get("/queue/{queue_id}", response_model=Queue)
async def get_queue(queue_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> Queue:
    return await crud.get_queue(session = session, queue_id = queue_id)


@router.post('/queue/{queue_id}')
async def add_to_queue(
    queue_id: int,
    form: AddQueueEntryForm,
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> None:
    return await crud.add_to_queue(session = session, queue_id = queue_id, form = form)

@router.post('/queue/{entry_id}')
async def remove_from_queue(
    entry_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> None:
    return await crud.remove_from_queue(session = session, entry_id = entry_id)

# @router.post("/month_stats/", response_model=TeacherMonthStats)
# async def get_teacher_month_stats(request: TeacherMonthStatsRequest,
#                                   session: AsyncSession = Depends(db_helper.session_dependency)):
#     return await crud.get_teacher_month_stats(date=request.date, teacher_id=request.teacher_id, session=session)
