from typing import List

from pydantic import BaseModel, ConfigDict, ValidationError


class MergeResult(BaseModel):
    model_config = ConfigDict(strict=True)
    result: str
    replaced_information: str
