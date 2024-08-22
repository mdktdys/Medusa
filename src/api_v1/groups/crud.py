"""
Read
"""

from datetime import datetime

from sqlalchemy.engine import Result
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import Group
from src.models.day_schedule_model import DaySchedule, Para
from src.models.paras_model import Paras


async def get_groups(session: AsyncSession) -> list[Group]:
    query = select(Group)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_by_id(session: AsyncSession, group_id: int) -> list[Group]:
    query = select(Group).where(Group.id == group_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_group_shedule_by_date(
    session: AsyncSession, group_id: int, date: datetime
) -> DaySchedule:
    query = select(Paras).where(Paras.group == group_id and Paras.date == date)
    result: Result = await session.execute(query)
    print(result)
    res = DaySchedule(
        paras=[
            Para(
                origin=Paras(
                    id=1,
                    group=1,
                    number=1,
                    course=1,
                    cabinet=1,
                    teacher=1,
                    date=datetime.now(),
                ),
                zamena=None,
            )
        ]
    )
    print("tet")
    return res
