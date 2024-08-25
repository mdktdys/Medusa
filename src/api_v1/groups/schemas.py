from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class GroupBase(BaseModel):
    id: int


class GroupGet:
    pass


class Paras(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: datetime

    def __init__(
        self,
        id: int,
        group_id: int,
        number_para: int,
        course_id: int,
        teacher_id: int,
        cabinet_id: int,
        date: datetime.date,
    ):
        self.id = id
        self.group_id = group_id
        self.number_para = number_para
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.cabinet_id = cabinet_id
        self.date = date


class Zamena(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: datetime

    def __init__(
        self,
        id: int,
        group_id: int,
        number_para: int,
        course_id: int,
        teacher_id: int,
        cabinet_id: int,
        date: datetime.date,
    ):
        self.id = id
        self.group_id = group_id
        self.number_para = number_para
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.cabinet_id = cabinet_id
        self.date = date


class Para(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    origin: Paras | None = None
    zamena: Paras | None = None


class Group(GroupBase):
    model_config = ConfigDict(from_attributes=True)
    name: str
    department: int


class DaySchedule(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    paras: List[Para]


class DayScheduleFormatted(BaseModel):
    search_name: str
    paras: str = ""
