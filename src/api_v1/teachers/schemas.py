import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from src.models.day_schedule_model import Para
from src.api_v1.groups.schemas import Para as ParaPydantic


class DayScheduleTeacher:
    search_name: str
    paras: List[List[Para | List]]

    def __init__(self, search_name, paras):
        self.search_name = search_name
        self.paras = paras


class DayScheduleTeacherPydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    search_name: str
    paras: List[List[ParaPydantic | List]]

    def __init__(self, search_name, paras):
        self.search_name = search_name
        self.paras = paras


class DayScheduleFormatted(BaseModel):
    subscribed: bool
    search_name: str
    full_zamena: bool
    paras: List[str] = []


class Teacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    synonyms: List[str]


class QueueStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    queue: Optional[int]
    position: Optional[int]
    student: Optional[str]
    creator_tg_id: Optional[str]
    created_at: datetime
    comment: Optional[str]
    teacher_comment: Optional[str]


class Queue(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    teacher: int
    students: List[QueueStudent]


class ZamenasFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    date: datetime.datetime


class TeacherMonthStats(BaseModel):
    teacher_id: int


class TeacherMonthStatsRequest(BaseModel):
    teacher_id: int
    date: datetime.date
