from datetime import datetime, timedelta
from typing import List
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from src.api_v1.groups.schemas import Zamena, Paras, DayScheduleFormatted
from src.api_v1.teachers.schemas import DayScheduleTeacher
from src.models.day_schedule_model import DaySchedule, Para
from src.utils.tools import get_number_para_emoji


async def get_teachers(session: AsyncSession) -> list[database.Teachers]:
    query = select(database.Teachers)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_teacher_by_id(
    session: AsyncSession, teacher_id: int
) -> list[database.Teachers]:
    query = select(database.Teachers).where(database.Teachers.id == teacher_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_teacher_day_schedule_by_date(
    session: AsyncSession, teacher_id: int, date: datetime
) -> DayScheduleTeacher:

    search_group: database.Teachers = list(
        (
            await session.execute(
                select(database.Teachers).where(database.Teachers.id == teacher_id)
            )
        )
        .scalars()
        .all()
    )[0]

    query = select(database.Paras).where(
        and_(database.Paras.teacher == teacher_id, database.Paras.date == date)
    )
    result: Result = await session.execute(query)
    paras_on_day: List[database.Paras] = list(result.scalars().all())
    query = select(database.Zamenas).where(
        and_(database.Zamenas.teacher == teacher_id, database.Zamenas.date == date)
    )
    result: Result = await session.execute(query)
    zamenas_on_day: List[database.Zamenas] = list(result.scalars().all())

    lessons_list: List[Para] = []
    for i in range(1, 8):
        lesson_origin = next((x for x in paras_on_day if x.number == i), None)
        lesson_zamena = next((x for x in zamenas_on_day if x.number == i), None)
        if lesson_zamena is not None or lesson_origin is not None:
            lessons_list.append(Para(origin=lesson_origin, zamena=lesson_zamena))

    res = DayScheduleTeacher(paras=lessons_list, search_name=search_group.name)
    return res


async def get_teacher_day_schedule_by_date_formatted(
    session: AsyncSession, teacher_id: int, date: datetime
) -> DayScheduleFormatted:
    schedule: DayScheduleTeacher = await get_teacher_day_schedule_by_date(
        session=session, teacher_id=teacher_id, date=date
    )
    rows = []
    for para in schedule.paras:
        if para.zamena is not None:
            if para.origin is None:
                rows.append(
                    f"\n{get_number_para_emoji(para.zamena.number)} {para.zamena.Courses_.fullname} <b>Замена🔄️</b>"
                    f"\n{para.zamena.Teachers_.name}️"
                    f"\n{para.zamena.scheduleTimetable.start}-{para.zamena.scheduleTimetable.end}   {para.zamena.Cabinets_.name}"
                )
            else:
                rows.append(
                    f"\n{get_number_para_emoji(para.zamena.number)} {para.zamena.Courses_.fullname} <b>Замена🔄️</b>"
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
    return DayScheduleFormatted(paras=rows, search_name=schedule.search_name)


async def get_teacher_week_schedule_by_date(
    session: AsyncSession, teacher_id: int, monday_date: datetime
) -> List[DaySchedule]:
    end_week = monday_date + timedelta(days=6)
    search_group: database.Groups = list(
        (
            await session.execute(
                select(database.Groups).where(database.Teachers.id == teacher_id)
            )
        )
        .scalars()
        .all()
    )[0]
    query = select(database.Zamenas).where(
        and_(
            database.Zamenas.teacher == teacher_id,
            database.Zamenas.date.between(monday_date, end_week),
        )
    )
    result: Result = await session.execute(query)
    paras_on_week: List[Paras] = list(result.scalars().all())
    query = select(database.Zamenas).where(
        and_(
            database.Zamenas.teacher == teacher_id,
            database.Zamenas.date.between(monday_date, end_week),
        )
    )
    result: Result = await session.execute(query)
    zamenas_on_week: List[Zamena] = list(result.scalars().all())

    week_lessons: List[DayScheduleTeacher] = []
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
            DayScheduleTeacher(paras=day_lessons_list, search_name=search_group.name)
        )
    return week_lessons
