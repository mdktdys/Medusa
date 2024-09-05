from typing import List

from pydantic import BaseModel, ConfigDict, ValidationError


class Teacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
