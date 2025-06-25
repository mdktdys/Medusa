from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class AlreadyFoundLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    link: str
    created_at: datetime
    date: date
    
    
class AlreadyFoundLinkFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
