import datetime
from io import BytesIO
from typing import List

import numpy as np
import pandas as pd

from src.parser.models.cabinet_model import Cabinet
from src.parser.models.course_model import Course
from src.parser.models.data_model import Data
from src.parser.models.group_model import Group
from src.parser.models.teacher_model import Teacher
from src.parser.parsers import init_date_model
from src.parser.schemas.paras import Paras
from src.parser.shared import (
    get_align_course_by_group,
    get_cabinet_from_string,
    get_course_from_string,
    get_group_from_string,
    get_teacher_from_string,
)
from src.parser.supabase import SupaBaseWorker


def parse_page(sheet: pd.DataFrame, data_model: Data, monday_date: datetime.date):
    rows: List[List] = sheet.values.tolist()
    paras: List[Paras] = []
    errors: List[str] = []

    rows.pop(0)
    rows.pop(0)
    rows.pop(0)
    rows.pop(0)
    rows.pop(1)

    for row in rows:
        row.pop(0)
        row.pop(0)

    groups_count = len(rows[0]) / 3

    if groups_count % 1 != 0:
        raise Exception("Groups count is not integer")

    for group_index in range(int(groups_count)):
        group_name = rows[0][0 + (group_index * 3)]

        for day_index in range(6):
            for para_index in range(7):
                course_name = rows[1 + (day_index * 7) + para_index][0 + (group_index * 3)]
                teacher_name = rows[1 + (day_index * 7) + para_index][1 + (group_index * 3)]
                cabinet_name = rows[1 + (day_index * 7) + para_index][2 + (group_index * 3)]

                if course_name is np.nan:
                    continue

                print(group_name, course_name, teacher_name, cabinet_name, para_index + 1, day_index)

                group: Group = get_group_from_string(group_name, data_model.GROUPS)
                course: Course | None = get_align_course_by_group(group, course_name, data_model)

                if course is None:
                    errors.append(f"Course not found {course_name} in {group_name}({group.id})")
                    continue

                teacher: Teacher | None = get_teacher_from_string(teacher_name, data_model.TEACHERS)

                if teacher is None:
                    errors.append(f"Teacher not found {teacher_name} in {group_name}")
                    continue

                cabinet: Cabinet = get_cabinet_from_string(cabinet_name, data_model.CABINETS)

                if cabinet is None:
                    errors.append(f"Cabinet not found {cabinet_name} in {group_name}")
                    continue

                date: datetime.date = monday_date + datetime.timedelta(days=day_index)

                paras.append(Paras(group=group.id, number=para_index + 1, course=course.id, teacher=teacher.id,
                                   cabinet=cabinet.id, date=date.strftime("%Y-%m-%d")))

    if len(errors) > 0:
        raise Exception(errors)

    return paras


def parse_schedule(bytes_: BytesIO, monday_date: datetime.date) -> List[Paras]:
    supabase_client = SupaBaseWorker()
    data_model = init_date_model(supabase_client)
    ex_data = pd.ExcelFile(bytes_)
    paras: List[Paras] = []

    for sheet_index in range(4):
        sheetX: pd.DataFrame = ex_data.parse(sheet_index)
        paras.extend(parse_page(sheet=sheetX, data_model=data_model, monday_date=monday_date))

    return paras


def parse_schedule_from_file(file_path: BytesIO, monday_date: datetime.date) -> List[Paras]:
    return parse_schedule(file_path, monday_date)

# paras: List[Paras] = parse_schedule_from_file("sample2.xlsx", monday_date=datetime.date(2025, 2, 3))
# print(paras)
# supabase_client = SupaBaseWorker()
# supabase_paras = []
#
# for para in paras:
#     print(para)
#     supabase_paras.append(
#         {
#             "group": para.group,
#             "number": para.number,
#             "course": para.course,
#             "teacher": para.teacher,
#             "cabinet": para.cabinet,
#             "date": para.date,
#         }
#     )
#
# res = supabase_client.client.table("Paras").insert(supabase_paras).execute()
# print(res)
