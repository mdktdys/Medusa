from typing import List

from pydantic import BaseModel

from src.alchemy.database import Groups


class FullDataDto(BaseModel):
    groups: List[Groups]