from typing import List

from pydantic import BaseModel, ConfigDict

from src.api_v1.groups.schemas import Para


class DayScheduleTeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    paras: List[List[Para]]


class DayScheduleFormatted(BaseModel):
    search_name: str
    paras: List[str] = []


class Teacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
