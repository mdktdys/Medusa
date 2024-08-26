import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from src.api_v1.groups.schemas import Para


class DayScheduleTeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    search_name: str
    paras: List[List[Para | List]]


class DayScheduleFormatted(BaseModel):
    search_name: str
    paras: List[str] = []


class Teacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ZamenasFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    date: datetime.datetime
