"""
Read
"""

from datetime import datetime, timedelta
from typing import List

from sqlalchemy.engine import Result
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import Group as AlchemyGroup
from src.alchemy import Paras as AlchemyParas
from src.alchemy import Zamena as AlchemyZamena
from src.api_v1.groups.schemas import Zamena, Paras
from src.models.day_schedule_model import DaySchedule, Para


async def get_groups(session: AsyncSession) -> list[AlchemyGroup]:
    query = select(AlchemyGroup)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_by_id(session: AsyncSession, group_id: int) -> list[AlchemyGroup]:
    query = select(AlchemyGroup).where(AlchemyGroup.id == group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_day_sсhedule_by_date(
    session: AsyncSession, group_id: int, date: datetime
) -> DaySchedule:

    # Get schedule
    query = select(AlchemyParas).where(
        (AlchemyParas.group == group_id) and (AlchemyParas.date == date)
    )
    result: Result = await session.execute(query)
    paras_on_day: List[AlchemyParas] = list(result.scalars().all())
    query = select(AlchemyZamena).where(
        (AlchemyZamena.group == group_id and AlchemyZamena.date == date)
    )
    result: Result = await session.execute(query)
    zamenas_on_day: List[AlchemyZamena] = list(result.scalars().all())

    lessons_list = []
    for i in range(1, 6):
        lesson_origin = next((x for x in paras_on_day if x.number == i), None)
        lesson_zamena = next((x for x in zamenas_on_day if x.number == i), None)
        if lesson_zamena is not None or lesson_origin is not None:
            lessons_list.append(Para(origin=lesson_origin, zamena=lesson_zamena))

    # Create final schedule
    res = DaySchedule(paras=lessons_list)

    return res


async def get_group_week_schedule_by_date(
    session: AsyncSession, group_id: int, monday_date: datetime
) -> List[DaySchedule]:

    end_week = monday_date + timedelta(days=6)

    # Get schedule
    query = select(AlchemyParas).where(
        (AlchemyParas.group == group_id)
        and (AlchemyParas.date.between(monday_date, end_week))
    )
    result: Result = await session.execute(query)
    paras_on_week: List[Paras] = list(result.scalars().all())
    query = select(AlchemyZamena).where(
        (
            AlchemyZamena.group == group_id
            and AlchemyZamena.date.between(monday_date, end_week)
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
        week_lessons.append(DaySchedule(paras=day_lessons_list))
    print("return")
    return week_lessons
