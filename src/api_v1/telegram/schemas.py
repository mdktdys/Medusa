from pydantic import BaseModel, ConfigDict
from typing import Optional

class Subscription(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    chat_id: str
    target_type: int
    target_id: int


class DaySchedule(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    

class AuthRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    token: str
    user_id: str
    chat_id: str
    photo_url: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None