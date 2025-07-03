from pydantic import BaseModel, ConfigDict


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
    photo_url: str
    username: str
    first_name: str
    last_name: str