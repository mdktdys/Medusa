from pydantic import BaseModel, ConfigDict
from datetime import date


class ZamenaRequest(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    date_from: date
    date_to: date


class ZamenaResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    practices: list
    cabinet_swaps: list
    zamenas_full: list
    zamena_file_links: list
    zamenas: list
    