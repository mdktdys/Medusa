from pydantic import BaseModel, ConfigDict


class CreateStateDto(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    token: str