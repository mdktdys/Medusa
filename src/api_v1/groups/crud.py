"""
Read
"""

from datetime import datetime, timedelta
from typing import List

from sqlalchemy.engine import Result
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession

# from src.alchemy import Group as AlchemyGroup
# from src.alchemy import Paras as AlchemyParas
# from src.alchemy import Zamena as AlchemyZamena
from src.alchemy import database
from src.api_v1.groups.schemas import Zamena, Paras, DayScheduleFormatted
from src.models.day_schedule_model import DaySchedule, Para


async def get_groups(session: AsyncSession) -> list[database.Groups]:
    query = select(database.Groups)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_by_id(
    session: AsyncSession, group_id: int
) -> list[database.Groups]:
    query = select(database.Groups).where(database.Groups.id == group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_day_schedule_by_date(
    session: AsyncSession, group_id: int, date: datetime
) -> DaySchedule:

    search_group: database.Groups = list(
        (
            await session.execute(
                select(database.Groups).where(database.Groups.id == group_id)
            )
        )
        .scalars()
        .all()
    )[0]
    query = select(database.Paras).where(
        and_(database.Paras.group == group_id, database.Paras.date == date)
    )
    result: Result = await session.execute(query)
    paras_on_day: List[database.Paras] = list(result.scalars().all())
    query = select(database.Zamenas).where(
        and_(database.Zamenas.group == group_id, database.Zamenas.date == date)
    )
    result: Result = await session.execute(query)
    zamenas_on_day: List[database.Zamenas] = list(result.scalars().all())

    lessons_list: List[Para] = []
    for i in range(1, 6):
        lesson_origin = next((x for x in paras_on_day if x.number == i), None)
        lesson_zamena = next((x for x in zamenas_on_day if x.number == i), None)
        if lesson_zamena is not None or lesson_origin is not None:
            lessons_list.append(Para(origin=lesson_origin, zamena=lesson_zamena))

    # Create final schedule
    res = DaySchedule(paras=lessons_list, search_name=search_group.name)
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
                rows.append(f"{para.zamena.Courses_.fullname} new\n")
            else:
                rows.append(f"{para.origin.Courses_.fullname} old\n")
                rows.append(f"{para.zamena.Courses_.fullname} new\n")
        else:
            rows.append(f"{para.origin.Courses_.fullname} old")

    return DayScheduleFormatted(paras="".join(rows), search_name=schedule.search_name)


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
