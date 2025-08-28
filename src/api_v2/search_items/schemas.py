from pydantic import BaseModel, ConfigDict


class SearchItemDto(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    uid: str
    name: str
