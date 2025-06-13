from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from sqlalchemy import Select, select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.data_source import DataSource
from src.alchemy import database
from sqlalchemy.orm import selectinload
from src.api_v1.groups.schemas import GroupScheduleRequest, GroupScheduleResponse, Paras, DayScheduleFormatted
from src.api_v1.telegram.crud import get_chat_subscribers
from src.models.day_schedule_model import Para
from src.utils.tools import get_number_para_emoji
from src.api_v1.teachers.schemas import ZamenasFull, DayScheduleTeacher, TeacherMonthStats, DayScheduleTeacherPydantic
from src.api_v1.groups.schemas import Zamena as Zamenas
import asyncio


async def get_teacher_queues(session: AsyncSession, teacher_id: int) -> List[database.Queue]:
    result: Result[Tuple[database.Queue]] = await session.execute(select(database.Queue).where(database.Queue.teacher == teacher_id))
    return list(result.scalars().all())


async def get_queue(session: AsyncSession, queue_id: int) -> Optional[database.Queue]:
    result: Result[Tuple[database.Queue]] = await session.execute(
        select(database.Queue)
        .options(selectinload(database.Queue.students))
        .where(database.Queue.id == queue_id)
    )

    queue: Optional[database.Queue] = result.scalar_one_or_none()
    return queue


async def get_teachers(session: AsyncSession) -> List[database.Teachers]:
    query: Select[Tuple[database.Teachers]] = select(database.Teachers)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_teacher_by_id(session: AsyncSession, teacher_id: int) -> List[database.Teachers]:
    query: Select[Tuple[database.Teachers]] = select(database.Teachers).where(database.Teachers.id == teacher_id)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_teacher_day_schedule_by_date(
    session: AsyncSession,
    teacher_id: int,
    date: datetime
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
        query = select(database.Paras).where(and_(database.Paras.teacher == teacher_id, database.Paras.date == date)).options(
            selectinload(database.Paras.Courses_),
            selectinload(database.Paras.Teachers_),
            selectinload(database.Paras.scheduleTimetable),
            selectinload(database.Paras.Cabinets_),
            selectinload(database.Paras.Groups_)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    async def get_teachers_zamenas_by_date() -> List[Zamenas]:
        query = select(database.Zamenas).where(and_(database.Zamenas.teacher == teacher_id, database.Zamenas.date == date)).options(
            selectinload(database.Zamenas.Courses_),
            selectinload(database.Zamenas.Teachers_),
            selectinload(database.Zamenas.scheduleTimetable),
            selectinload(database.Zamenas.Cabinets_),
            selectinload(database.Zamenas.Groups_)
        )
        result: Result = await session.execute(query)
        return list(result.scalars().all())

    async def get_groups_zamenas_full_by_date(zamenas_on_day: List[Zamenas]) -> List[ZamenasFull]:
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

    full_zamenas: List[ZamenasFull] = await get_groups_zamenas_full_by_date(zamenas_on_day = zamenas_on_day)

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
    session: AsyncSession,
    teacher_id: int,
    date: datetime,
    chat_id: int
) -> DayScheduleFormatted:
    schedule: DayScheduleTeacher = await get_teacher_day_schedule_by_date(
        session=session, teacher_id=teacher_id, date=date
    )
    rows = []
    subscribed = any(
        [
            True
            for sub in (await get_chat_subscribers(chat_id=chat_id, session=session))
            if sub.target_id == teacher_id and sub.target_type == 2
        ]
    )
    for paras in schedule.paras:
        if (len(paras)) != 0:
            for para in paras:
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
    return DayScheduleFormatted(
        paras=rows,
        search_name=schedule.search_name,
        full_zamena=False,
        subscribed=subscribed,
    )


async def get_teacher_week_schedule_by_date(
        session: AsyncSession, teacher_id: int, monday_date: datetime
) -> List[DayScheduleTeacherPydantic]:
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
        week_lessons.append(day_lessons_list)
    return week_lessons


async def get_teacher_month_stats(date: datetime, teacher_id: int, session: AsyncSession) -> TeacherMonthStats:
    return TeacherMonthStats(teacher_id = teacher_id)
    

async def get_teacher_schedule(
    request: GroupScheduleRequest,
    datasource: DataSource
) -> GroupScheduleResponse:

    return GroupScheduleResponse(schedule=[])


# Future<List<DaySchedule>> teacherSchedule({
#     required final List<LessonTimings> timings,
#     required final DateTime startdate,
#     required final Teacher searchItem,
#     required final DateTime endDate,
#   }) async {

#     final List<Lesson> lessons = (await Api.loadWeekTeacherSchedule(
#       teacherID: searchItem.id,
#       start: startdate,
#       end: endDate,
#     ))..sort((final a, final b) => a.date.compareTo(b.date));

#     final List<int> groups = List<int>.from(lessons.map((final Lesson e) => e.group));
    
#     final result = await Future.wait([
#       Api.getZamenasFull(groups, startdate, endDate),
#       Api.getLiquidation(groups, startdate, endDate),
#       Api.loadZamenas(groupsID: groups, start: startdate, end: endDate),
#       Api.getZamenaFileLinks(start: startdate, end: endDate),
#       Api.getAlreadyFoundLinks(start: startdate, end: endDate),
#       Api.getHolidays(startdate, endDate)
#     ].toList());

#     final List<ZamenaFull> zamenasFull = result[0] as List<ZamenaFull>;
#     // final List<Liquidation> liquidations = result[1] as List<Liquidation>;
#     final List<Zamena> groupsLessons = result[2] as List<Zamena>;
#     final List<ZamenaFileLink> links = result[3] as List<ZamenaFileLink>;
#     final List<TelegramZamenaLinks> telegramLinks = result[4] as List<TelegramZamenaLinks>;
#     final List<Holiday> holidays = result[5] as List<Holiday>;

#     List<DaySchedule> schedule = [];
#     for (DateTime date in List.generate(math.max(endDate.difference(startdate).inDays, 1), (final int index) => startdate.add(Duration(days: index)))) {
#       List<Paras> dayParas = [];

#       final List<Lesson> teacherDayLessons = lessons.where((final lesson) => lesson.date.sameDate(date)).toList();
#       final List<Zamena> dayGroupsLessons = groupsLessons.where((final lesson) => lesson.date.sameDate(date)).toList();

#       for (LessonTimings timing in timings) {
#         final Paras paras = Paras();

#         final List<Lesson> teacherLesson = teacherDayLessons.where((final Lesson lesson) => lesson.number == timing.number).toList();
#         final List<Zamena> groupLessonZamena = dayGroupsLessons.where((final Zamena lesson) => lesson.lessonTimingsID == timing.number).toList();
#         final List<ZamenaFull> paraZamenaFull = zamenasFull.where((final zamena) => zamena.date.sameDate(date)).toList();

#         paras.lesson = teacherLesson;
#         paras.zamena = groupLessonZamena;
#         paras.zamenaFull = paraZamenaFull;

#         if (
#           paras.lesson!.isEmpty
#           && paras.zamena!.isEmpty
#         ) {
#           continue;
#         }

#         paras.number = timing.number;
#         dayParas.add(paras);
#       }

#       final DaySchedule daySchedule = DaySchedule(
#         zamenaFull: null,
#         holidays: holidays.where((final holiday) => holiday.date.sameDate(date)).toList(),
#         telegramLink: telegramLinks.where((final link) => link.date.sameDate(date)).firstOrNull,
#         zamenaLinks: links.where((final link) => link.date.sameDate(date)).toList(),
#         paras: dayParas,
#         date: date,
#       );

#       schedule.add(daySchedule);
#     }

#     return schedule;
#   }