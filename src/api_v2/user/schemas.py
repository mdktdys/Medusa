from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    first_name: str
    last_name: str
    username: str
    role: str