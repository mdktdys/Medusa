import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class Cabinet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    synonyms: List[str]
