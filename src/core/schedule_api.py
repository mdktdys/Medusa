import datetime
from typing import List, Tuple

from src.core.supabase_connect import supabase_connect
from src.core.tools import get_week_start_end, weekdays_names, get_course_by_id,get_teacher_by_id
from src.models.models import *


def get_group_default_schedule_formatted(group_id: int, week_number: int) -> str:
    paras = get_group_default_schedule(group_id=group_id, week_number=week_number)
    result = ""
    for day_number in range(0, 6):
        result = f"{result + weekdays_names[day_number+1]}\n"
        day_paras = [x for x in paras if x.date.weekday() == day_number]
        for para in day_paras:
            result = result + f"{para.number_para}|{get_course_by_id(para.course_id).name}|{get_teacher_by_id(para.teacher_id).name}\n"

    return result


def get_group_default_schedule(group_id: int, week_number: int) -> list[Paras]:
    start_week_date_moday, start_week_date_sundy = get_week_start_end(week_number, 2023)
    response: List[dict] = supabase_connect.table('Paras').select('*').eq('group', group_id).gte('date',
                                                                                                 start_week_date_moday).lte(
        'date', start_week_date_sundy).execute().data
    paras: List[Paras] = []
    for i in response:
        para = para_map_to_model(i)
        paras.append(para)
    return paras


def get_group_default_schedule_json(group_id: int, week_number: int) -> dict[int,List[dict]]:
    paras = get_group_default_schedule(group_id=group_id,week_number=week_number)
    schudule = {}
    for day_number in range(0, 6):
        schudule[day_number + 1] = [x.toDict() for x in paras if x.date.weekday() == day_number]
    return schudule


def para_map_to_model(data: dict) -> Paras:
    return Paras(id=data['id'], group_id=data['group'], number_para=data['number'], course_id=data['course'],
                 teacher_id=data['teacher'], cabinet_id=data['cabinet'], date=datetime.datetime.strptime(data['date'], "%Y-%m-%d"))
