from datetime import datetime, timedelta
from typing import List
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from src.api_v1.groups.schemas import Paras, DayScheduleFormatted
from src.models.day_schedule_model import DaySchedule, Para
from src.utils.tools import get_number_para_emoji
from src.api_v1.teachers.schemas import ZamenasFull, DayScheduleTeacher
from src.api_v1.groups.schemas import Zamena as Zamenas
import asyncio


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

    async def get_search_teacher() -> database.Teachers:
        return list(
            (
                await session.execute(
                    select(database.Teachers)
                    .where(database.Teachers.id == teacher_id)
                    .limit(1)
                )
            )
            .scalars()
            .all()
        )[0]

    async def get_teachers_origin_paras_by_date() -> List[Paras]:
        query = select(database.Paras).where(
            and_(database.Paras.teacher == teacher_id, database.Paras.date == date)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    async def get_teachers_zamenas_by_date() -> List[Zamenas]:
        query = select(database.Zamenas).where(
            and_(database.Zamenas.teacher == teacher_id, database.Zamenas.date == date)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    async def get_groups_zamenas_full_by_date(
        zamenas_on_day: List[Zamenas],
    ) -> List[ZamenasFull]:
        query = select(database.ZamenasFull).where(
            and_(
                database.ZamenasFull.group.in_([x.group for x in zamenas_on_day]),
                database.ZamenasFull.date == date,
            )
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    teacher_task, paras_on_day, zamenas_on_day = await asyncio.gather(
        get_search_teacher(),
        get_teachers_origin_paras_by_date(),
        get_teachers_zamenas_by_date(),
    )

    full_zamenas: List[ZamenasFull] = await get_groups_zamenas_full_by_date(
        zamenas_on_day=zamenas_on_day
    )

    lessons_list: List[List[Para | List]] = [[] for i in range(0, 7)]
    for i in range(1, 8):
        lesson_origin = [x for x in paras_on_day if x.number == i]
        lesson_zamena = [x for x in zamenas_on_day if x.number == i]

        if len(lesson_zamena) == 0:
            if len(lesson_origin) != 0:
                for lesson in lesson_origin:
                    if len([x for x in full_zamenas if x.group == lesson.group]) == 0:
                        lessons_list[i - 1].append(Para(origin=lesson, zamena=None))
        else:
            if len(lesson_origin) == 0:
                for zamena in lesson_zamena:
                    lessons_list[i - 1].append(Para(zamena=zamena, origin=None))
            else:
                for lesson in lesson_origin:
                    if len([x for x in full_zamenas if x.group == lesson.group]) == 0:
                        lessons_list[i - 1].append(Para(zamena=None, origin=lesson))
                for zamena in lesson_zamena:
                    lessons_list[i - 1].append((Para(zamena=zamena, origin=None)))

    return DayScheduleTeacher(paras=lessons_list, search_name=teacher_task.name)


async def get_teacher_day_schedule_by_date_formatted(
    session: AsyncSession, teacher_id: int, date: datetime
) -> DayScheduleFormatted:
    schedule: DayScheduleTeacher = await get_teacher_day_schedule_by_date(
        session=session, teacher_id=teacher_id, date=date
    )
    rows = []
    print(type(schedule))
    for paras in schedule.paras:
        if (len(paras)) != 0:
            for para in paras:
                print(type(para))
                if isinstance(para, Para):
                    if para.origin is None:
                        rows.append(
                            f"\n{get_number_para_emoji(para.zamena.number)} {para.zamena.Courses_.fullname} <b>Замена🔄️</b>"
                            f"\n{para.zamena.Groups_.name}️"
                            f"\n{para.zamena.scheduleTimetable.start}-{para.zamena.scheduleTimetable.end}   {para.zamena.Cabinets_.name}"
                        )
                        # else:
                        #     rows.append(
                        #         f"\n{get_number_para_emoji(para.zamena.number)} {para.zamena.Courses_.fullname} <b>Замена🔄️</b>"
                        #     )
                        #     rows.append(
                        #         f"{para.zamena.Teachers_.name}"
                        #         f"\n{para.zamena.scheduleTimetable.start}-{para.zamena.scheduleTimetable.end}   {para.zamena.Cabinets_.name}"
                        #     )
                        #     rows.append(
                        #         f"<s>"
                        #         f"\n{para.origin.Courses_.fullname}"
                        #         f"\n{para.origin.Teachers_.name}"
                        #         f"\n{para.origin.scheduleTimetable.start}-{para.origin.scheduleTimetable.end}   {para.origin.Cabinets_.name}</s>"
                        #     )
                    else:
                        rows.append(
                            f"\n{get_number_para_emoji(para.origin.number)} {para.origin.Courses_.fullname}"
                            f"\n{para.origin.Groups_.name}"
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
    zamenas_on_week: List[Zamenas] = list(result.scalars().all())

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
