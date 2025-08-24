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