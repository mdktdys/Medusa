from pydantic import BaseModel, ConfigDict


class Department(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    name: str
    
    
class DepartmentCreate(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    name: str