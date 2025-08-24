from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateStateDto(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    token: str
    

class AuthStatusDto(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    access_token: str
    refresh_token: str
    

class AuthStatusRequest(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    token: str
    
    
class AuthRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    token: str
    user_id: str
    chat_id: str
    photo_url: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    
class AuthDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    result: str