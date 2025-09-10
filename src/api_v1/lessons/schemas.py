from datetime import date
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator


class Lesson(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    group_id: int
    number: int
    discipline_id: int
    teacher_id: Optional[int]
    cabinet_id: Optional[int]
    date: date
    
    
class LessonFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    group: Union[List[int], None] = None
    number: Optional[int] = None
    course: Optional[int] = None
    teacher: Optional[int] = None
    cabinet: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    @field_validator("group", mode="before")
    @classmethod
    def ensure_list(cls, v):
        if v is None:
            return None
        if isinstance(v, list):
            return v
        return [v]
    