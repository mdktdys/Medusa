from datetime import datetime, date
from typing import List

from pydantic import BaseModel, ConfigDict


class Paras(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: datetime


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
    
class GroupScheduleResponse(BaseModel):
    schedule: list