from datetime import datetime, date
from typing import List

from pydantic import BaseModel, ConfigDict

from src.models.holiday_model import Holiday
from src.models.paras_model import Paras
from src.models.zamena_file_link_model import ZamenaFileLink
from src.models.zamena_full import ZamenaFull
from src.models.zamenas import Zamenas


# class Paras(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     id: int
#     group: int
#     number: int
#     course: int
#     teacher: int
#     cabinet: int
#     date: datetime


class Zamena(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: datetime


class Para(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    origin: Paras | None = None
    zamena: Paras | None = None


class Group(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    department: int
    

class DaySchedule(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    paras: List[Para]


class DayScheduleFormatted(BaseModel):
    subscribed: bool
    search_name: str
    full_zamena: bool
    paras: List[str] = []
    

class GroupScheduleRequest(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    group_id: int
    date_from: date
    date_to: date

class ScheduleLesson(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    number: int    
    lessons: list[Paras]
    zamenas: list[Zamenas]

class ScheduleDaySchedule(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    date: date
    paras: list[ScheduleLesson]
    holidays: list[Holiday]
    zamena_full: ZamenaFull | None
    telegram_link: ZamenaFileLink | None
    zamena_links: list[ZamenaFileLink]

class GroupScheduleResponse(BaseModel):
    schedule: list[ScheduleDaySchedule]
    
class GroupCreate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    name: str
    department: int
    