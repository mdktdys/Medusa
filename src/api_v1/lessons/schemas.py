from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from typing import Union, List

class Lesson(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
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
    