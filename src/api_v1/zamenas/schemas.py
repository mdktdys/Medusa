from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional

class Zamena(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: date
    
    
class ZamenaFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    group: Optional[int] = None
    number: Optional[int] = None
    course: Optional[int] = None
    teacher: Optional[int] = None
    cabinet: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    