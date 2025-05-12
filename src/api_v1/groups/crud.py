from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.alchemy import database
from src.api_v1.groups.schemas import DayScheduleFormatted
from src.api_v1.telegram.crud import (
    get_chat_subscribers,
)
from src.models.day_schedule_model import DaySchedule, Para
from src.utils.tools import get_number_para_emoji
from .schemas import Group

async def get_groups(session: AsyncSession) -> list[Group]:
    query = select(database.Groups)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_by_id(
        session: AsyncSession, group_id: int
) -> list[Group]:
    query = select(database.Groups).where(database.Groups.id == group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


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
    ).options(selectinload(database.Paras.Courses_))
    result: Result = await session.execute(query)
    paras_on_day: List[database.Paras] = list(result.scalars().all())

    # Get Zamenas
    query = select(database.Zamenas).where(
        and_(database.Zamenas.group == group_id, database.Zamenas.date == date)
    ).options(selectinload(database.Zamenas.Courses_))
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
    subscribed = any(
        [
            True
            for sub in (await get_chat_subscribers(chat_id=chat_id, session=session))
            if sub.target_id == group_id and sub.target_type == 1
        ]
    )
    
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
        subscribed=subscribed,
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
