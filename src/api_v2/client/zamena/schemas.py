from datetime import date

from pydantic import BaseModel, ConfigDict

from src.api_v1.zamena_file_links.schemas import ZamenaFileLink
from src.api_v1.zamenas.schemas import ZamenaSwap
from src.api_v1.zamenas_full.schemas import ZamenasFull


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
    zamenas: list[ZamenaSwap]
    