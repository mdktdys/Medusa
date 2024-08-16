import datetime
from typing import Tuple

from src.core.data import database_data
from src.models.models import *

weekdays_names = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
}


def get_week_start_end(
    week_number: int, year: int
) -> Tuple[datetime.date, datetime.date]:
    first_day_of_year = datetime.datetime(year, 9, 1)
    first_day_of_week = first_day_of_year.isoweekday()
    days_difference = first_day_of_week - 1
    week_start = (
        first_day_of_year
        - datetime.timedelta(days=days_difference)
        + datetime.timedelta(weeks=week_number - 1)
    )
    week_end = week_start + datetime.timedelta(days=6)
    return week_start.date(), week_end.date()


def get_next_day_number() -> int:
    return datetime.datetime.now().weekday()


def get_group_by_id(group_id: int) -> Group:
    return [group for group in database_data.GROUPS if group.id == group_id][0]


def get_course_by_id(course_id: int) -> Course:
    return [course for course in database_data.COURSES if course.id == course_id][0]


def get_teacher_by_id(teacher_id: int) -> Course:
    return [teacher for teacher in database_data.TEACHERS if teacher.id == teacher_id][
        0
    ]
