from typing import Optional

from pydantic import BaseModel


class LoadLinkersRequest(BaseModel):
    group_id: int
    
    
class CreateLoadLinkRequest(BaseModel):
    first_year_hours: Optional[int]
    second_year_hours: Optional[int]
    teacher_id: Optional[int]
    discipline_code_id: Optional[int]
    discipline_id: Optional[int]
    group_id: int