from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from typing import Union, List

from src.alchemy.database_local import ZamenaGroupType

class CreateZamenaRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    saturday_timings: Optional[bool] = False
    file_url: Optional[str] = None
    file_hash: Optional[str] = None
    date: date


class ZamenaSwap(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    zamena_id: int
    group_id: int
    number: int
    course_id: int
    teacher_id: int
    cabinet_id: int
    date: date

class ZamenaGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    zamena_id: int
    group_id: int
    type: ZamenaGroupType
    
class ZamenaFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None