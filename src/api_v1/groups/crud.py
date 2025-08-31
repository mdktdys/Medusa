import asyncio
from datetime import datetime, timedelta
from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy import Result, Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import src.alchemy.database_local as database_local
from src.alchemy import database
from src.api_v1.groups.schemas import DayScheduleFormatted
from src.api_v1.telegram.crud import get_chat_subscribers
from src.data.data_source import DataSource
from src.models.day_schedule_model import DaySchedule, Para
from src.models.holiday_model import Holiday
from src.models.paras_model import Paras
from src.models.zamena_file_link_model import ZamenaFileLink
from src.models.zamena_full import ZamenaFull
from src.models.zamenas import Zamenas
from src.utils.tools import get_number_para_emoji

from .schemas import (CreateGroupRequest, Group, GroupScheduleRequest,
                      GroupScheduleResponse, ScheduleDaySchedule,
                      ScheduleLesson)


async def get_groups(session: AsyncSession) -> list[database.Groups]:
    query: Select[Tuple[database.Groups]] = select(database.Groups)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_by_id(session: AsyncSession, group_id: int) -> list[Group]:
    query: Select[Tuple[database.Groups]] = select(database.Groups).where(database.Groups.id == group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def update_group(
    session: AsyncSession,
    group_id: int,
    data: Group
) -> Group:
    query: Select[Tuple[database.Groups]] = select(database.Groups).where(database.Groups.id == group_id)
    result: Result[Tuple[database.Groups]] = await session.execute(query)
    group: database.Groups | None = result.scalar_one_or_none()

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(group, key, value)

    await session.commit()
    await session.refresh(group)
    return group # type: ignore


async def delete_group(session: AsyncSession, group_id: int) -> dict[str, str]:
    query: Select[Tuple[database.Groups]] = select(database.Groups).where(database.Groups.id == group_id)
    result: Result[Tuple[database.Groups]] = await session.execute(query)
    group: database.Groups | None = result.scalar_one_or_none()

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    await session.delete(group)
    await session.commit()
    return {"result": "ok"}


async def create_group(session: AsyncSession, data: CreateGroupRequest) -> Group:
    new_group = database_local.Group(**data.model_dump(exclude={"id"}))
    session.add(new_group)
    await session.commit()
    await session.refresh(new_group)
    return new_group # type: ignore


# Schedule
async def get_group_day_schedule_by_date(session: AsyncSession, group_id: int, date: datetime
) -> DaySchedule:
    # Get Group
    search_group: database.Groups = list(
        (
            await session.execute(
                select(database.Groups).where(database.Groups.id == group_id).limit(1)
            )
        )
        .scalars()
        .all()
    )[0]

    # Get Paras
    query = select(database.Paras).where(
        and_(database.Paras.group == group_id, database.Paras.date == date)
    ).options(
        selectinload(database.Paras.Courses_),
        selectinload(database.Paras.Teachers_),
        selectinload(database.Paras.scheduleTimetable),
        selectinload(database.Paras.Cabinets_)
    )
    result: Result = await session.execute(query)
    paras_on_day: List[database.Paras] = list(result.scalars().all())

    # Get Zamenas
    query = select(database.Zamenas).where(
        and_(database.Zamenas.group == group_id, database.Zamenas.date == date)
    ).options(
        selectinload(database.Zamenas.Courses_),
        selectinload(database.Zamenas.Teachers_),
        selectinload(database.Zamenas.scheduleTimetable),
        selectinload(database.Zamenas.Cabinets_)
    )
    result: Result = await session.execute(query)
    zamenas_on_day: List[database.Zamenas] = list(result.scalars().all())

    # Get FullZamenas
    query = select(database.ZamenasFull).where(
        and_(
            database.ZamenasFull.group == search_group.id,
            database.ZamenasFull.date == date,
        )
    )
    result: Result = await session.execute(query)
    full_zamenas: List[database.ZamenasFull] = list(result.scalars().all())
    is_full_zamena = len(full_zamenas) != 0

    if not is_full_zamena:
        lessons_list: List[Para] = []
        for i in range(1, 8):
            lesson_origin = next((x for x in paras_on_day if x.number == i), None)
            lesson_zamena = next((x for x in zamenas_on_day if x.number == i), None)
            if lesson_zamena is not None or lesson_origin is not None:
                lessons_list.append(Para(origin=lesson_origin, zamena=lesson_zamena))

    else:
        lessons_list: List[Para] = []
        for i in range(1, 8):
            lesson_origin = next((x for x in zamenas_on_day if x.number == i), None)
            if lesson_origin is not None:
                lessons_list.append(Para(origin=lesson_origin, zamena=None))

    res = DaySchedule(paras=lessons_list, search_name=search_group.name, full_zamena=is_full_zamena)
    return res


async def get_group_day_schedule_by_date_formatted(
    session: AsyncSession,
    group_id: int,
    date: datetime,
    chat_id: int,
) -> DayScheduleFormatted:
    schedule: DaySchedule = await get_group_day_schedule_by_date(session = session, group_id=group_id, date=date)
    rows = []
    subscribed = any([True for sub in (await get_chat_subscribers(chat_id=chat_id, session=session)) if sub.target_id == group_id and sub.target_type == 1])
    
    for para in schedule.paras:
        if para.zamena is not None:
            if para.origin is None:
                rows.append(
                    f"\n<b>Замена🔄️</b>️"
                    f"\n{get_number_para_emoji(para.zamena.number)} {para.zamena.Courses_.fullname}"
                    f"\n{para.zamena.Teachers_.name}️"
                    f"\n{para.zamena.scheduleTimetable.start}-{para.zamena.scheduleTimetable.end}   {para.zamena.Cabinets_.name}"
                )
            else:
                rows.append("\n<b>Замена🔄️</b>")
                rows.append(
                    f"\n{get_number_para_emoji(para.zamena.number)} {para.zamena.Courses_.fullname}"
                )
                rows.append(
                    f"{para.zamena.Teachers_.name}"
                    f"\n{para.zamena.scheduleTimetable.start}-{para.zamena.scheduleTimetable.end}   {para.zamena.Cabinets_.name}"
                )
                rows.append(
                    f"<s>"
                    f"\n{para.origin.Courses_.fullname}"
                    f"\n{para.origin.Teachers_.name}"
                    f"\n{para.origin.scheduleTimetable.start}-{para.origin.scheduleTimetable.end}   {para.origin.Cabinets_.name}</s>"
                )
        else:
            rows.append(
                f"\n{get_number_para_emoji(para.origin.number)} {para.origin.Courses_.fullname}"
                f"\n{para.origin.Teachers_.name}"
                f"\n{para.origin.scheduleTimetable.start}-{para.origin.scheduleTimetable.end}   {para.origin.Cabinets_.name}"
            )
    return DayScheduleFormatted(
        paras=rows,
        search_name=schedule.search_name,
        full_zamena=schedule.full_zamena,
        subscribed = subscribed,
    )


async def get_group_week_schedule_by_date(session: AsyncSession, group_id: int, monday_date: datetime) -> List[
    DaySchedule]:
    week_schedule: List[DaySchedule] = []

    for day in range(0, 6):
        current_date = monday_date + timedelta(days=day)
        day_schedule = await get_group_day_schedule_by_date(
            group_id=group_id, date=current_date, session=session
        )
        week_schedule.append(day_schedule)

    return week_schedule


async def get_group_schedule(
    request: GroupScheduleRequest,
    datasource: DataSource
) -> GroupScheduleResponse:
    lessons_task = datasource.get_lessons(
        group_id = request.group_id,
        date_from = request.date_from,
        date_to = request.date_to,
    )
    zamenas_task = datasource.get_zamenas(
        group_id = request.group_id,
        date_from = request.date_from,
        date_to = request.date_to,
    )
    zamena_file_links_task = datasource.get_zamena_file_links(
        date_from = request.date_from,
        date_to = request.date_to,
    )
    zamena_full_task = datasource.get_zamena_full(
        group_ids = [request.group_id],
        date_from = request.date_from,
        date_to = request.date_to,
    )
    holidays_task = datasource.get_holidays(
        date_from = request.date_from,
        date_to = request.date_to,
    )
    
    lessons, zamenas, zamena_file_links, zamena_full, holidays = await asyncio.gather(
        lessons_task,
        zamenas_task,
        zamena_file_links_task,
        zamena_full_task,
        holidays_task
    )
    
    day_count: int = max((request.date_to - request.date_from).days, 1)
    schedule = []
        
    for i in range(day_count):
        current_date = request.date_from + timedelta(days=i)

        day_lessons: List[Paras] = [lesson for lesson in lessons if lesson.date == current_date]
        day_zamenas: List[Zamenas] = [z for z in zamenas if z.date == current_date]
        day_zamena_full: ZamenaFull | None = next((z for z in zamena_full if z.date == current_date), None)
        # see
        day_telegram_link: ZamenaFileLink | None = next((t for t in zamena_file_links if t.date == current_date), None)
        day_zamena_links: List[ZamenaFileLink] = [z for z in zamena_file_links if z.date == current_date]
        day_holidays: List[Holiday] = [h for h in holidays if h.date == current_date]

        day_paras: list[ScheduleLesson] = []
        for timing in datasource.timings:
            lesson_matches: List[Paras] = [lesson for lesson in day_lessons if lesson.number == timing.number]
            zamena_matches: List[Zamenas] = [zamena for zamena in day_zamenas if zamena.number == timing.number and zamena.group == request.group_id]

            if not lesson_matches and not zamena_matches:
                continue

            paras = ScheduleLesson(
                number = timing.number,
                lessons = lesson_matches,
                zamenas = zamena_matches
            )
            day_paras.append(paras)

        day_schedule = ScheduleDaySchedule(
            date = current_date,
            paras = day_paras,
            holidays = day_holidays,
            zamena_full = day_zamena_full,
            telegram_link = day_telegram_link,
            zamena_links = day_zamena_links
        )

        schedule.append(day_schedule)

    return GroupScheduleResponse(schedule=schedule)