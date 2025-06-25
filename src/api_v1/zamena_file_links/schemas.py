from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ZamenaFileLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    link: str
    date: date
    created_at: datetime
    
    
class ZamenaFileLinksFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
