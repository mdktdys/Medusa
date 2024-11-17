from datetime import datetime, timedelta
from typing import List
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from src.api_v1.groups.schemas import Zamena, Paras, DayScheduleFormatted
from src.models.day_schedule_model import DaySchedule, Para
from src.utils.tools import get_number_para_emoji


async def get_groups(session: AsyncSession) -> List[database.Groups]:
    query = select(database.Groups)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_by_id(
    session: AsyncSession, group_id: int
) -> List[database.Groups]:
    query = select(database.Groups).where(database.Groups.id == group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_day_schedule_by_date(
    session: AsyncSession, group_id: int, date: datetime
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
    )
    result: Result = await session.execute(query)
    paras_on_day: List[database.Paras] = list(result.scalars().all())

    # Get Zamenas
    query = select(database.Zamenas).where(
        and_(database.Zamenas.group == group_id, database.Zamenas.date == date)
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

    if not is_full_zamena == 0:
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
            lessons_list.append(Para(origin=lesson_origin, zamena=None))

    res = DaySchedule(
        paras=lessons_list, search_name=search_group.name, full_zamena=is_full_zamena
    )
    return res


async def get_group_day_schedule_by_date_formatted(
    session: AsyncSession, group_id: int, date: datetime
) -> DayScheduleFormatted:
    schedule: DaySchedule = await get_group_day_schedule_by_date(
        session=session, group_id=group_id, date=date
    )
    rows = []
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
                rows.append(f"\n<b>Замена🔄️</b>")
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
        paras=rows, search_name=schedule.search_name, full_zamena=schedule.full_zamena
    )


async def get_group_week_schedule_by_date(
    session: AsyncSession, group_id: int, monday_date: datetime
) -> List[DaySchedule]:
    end_week = monday_date + timedelta(days=6)
    search_group: database.Groups = list(
        (
            await session.execute(
                select(database.Groups).where(database.Groups.id == group_id)
            )
        )
        .scalars()
        .all()
    )[0]
    query = select(database.Zamenas).where(
        and_(
            database.Zamenas.group == group_id,
            database.Zamenas.date.between(monday_date, end_week),
        )
    )
    result: Result = await session.execute(query)
    paras_on_week: List[Paras] = list(result.scalars().all())
    query = select(database.Zamenas).where(
        and_(
            database.Zamenas.group == group_id,
            database.Zamenas.date.between(monday_date, end_week),
        )
    )
    result: Result = await session.execute(query)
    zamenas_on_week: List[Zamena] = list(result.scalars().all())

    week_lessons: List[DaySchedule] = []
    for day in range(0, 6):
        current_date = monday_date + timedelta(days=day)
        day_paras = [
            paras for paras in paras_on_week if paras.date.day == current_date.day
        ]
        day_zamenas = [
            zamena for zamena in zamenas_on_week if zamena.date.day == current_date.day
        ]
        day_lessons_list = []
        for i in range(1, 6):
            lesson_origin = next((x for x in day_paras if x.number == i), None)
            lesson_zamena = next((x for x in day_zamenas if x.number == i), None)
            if lesson_zamena is not None or lesson_origin is not None:
                day_lessons_list.append(
                    Para(origin=lesson_origin, zamena=lesson_zamena)
                )
        week_lessons.append(
            DaySchedule(paras=day_lessons_list, search_name=search_group.name)
        )
    return week_lessons
