from typing import List

from src.core.supabase_connect import supabase_connect
from src.models.models import *


def get_teachers(sup) -> List[Teacher]:
    data, count = sup.table("Teachers").select("id", "name").execute()
    return [Teacher(item["id"], item["name"]) for item in data[1]]


def get_cabinets(sup) -> List[Cabinet]:
    data, count = sup.table("Cabinets").select("id", "name").execute()
    return [Cabinet(item["id"], item["name"]) for item in data[1]]


def get_groups(sup) -> List[Group]:
    data, count = sup.table("Groups").select("id", "name").execute()
    return [Group(item["id"], item["name"]) for item in data[1]]


def get_courses(sup) -> List[Course]:
    data, count = sup.table("Courses").select("id", "name").execute()
    return [Course(item["id"], item["name"]) for item in data[1]]


class Data:
    GROUPS: List[Group] = []
    CABINETS: List[Cabinet] = []
    TEACHERS: List[Teacher] = []
    COURSES: List[Course] = []

    def __init__(self, sup):
        self.GROUPS: List[Group] = get_groups(sup=sup)
        self.CABINETS: List[Cabinet] = get_cabinets(sup=sup)
        self.TEACHERS: List[Teacher] = get_teachers(sup=sup)
        self.COURSES: List[Course] = get_courses(sup=sup)


database_data = Data(sup=supabase_connect)
