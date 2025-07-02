from pydantic import BaseModel, ConfigDict
from datetime import date
from src.api_v1.zamenas_full.schemas import ZamenasFull
from src.api_v1.zamena_file_links.schemas import ZamenaFileLink
from src.api_v1.zamenas.schemas import Zamena

class ZamenaRequest(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    date_from: date
    date_to: date


class ZamenaResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    practices: list
    cabinet_swaps: list
    zamenas_full: list[ZamenasFull]
    zamena_file_links: list[ZamenaFileLink]
    zamenas: list[Zamena]
    