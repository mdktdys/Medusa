from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Union, List


class ZamenasFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group: int
    date: date
    
    
class ZamenasFullFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    group: Union[List[int], None] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    @field_validator("group", mode="before")
    @classmethod
    def ensure_list(cls, v) -> None | list:
        if v is None:
            return None
        if isinstance(v, list):
            return v
        return [v]
    