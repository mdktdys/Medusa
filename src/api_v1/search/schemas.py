from typing import List

from pydantic import BaseModel, ConfigDict, ValidationError

class SearchResult(BaseModel):
    model_config = ConfigDict(strict=True)
    search_image: str
    search_type: str
    search_name: str
    search_id: int
