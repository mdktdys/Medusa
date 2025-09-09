from datetime import date
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel
from pydantic_core import Url


class ParseZamenaRequest(BaseModel):
    url: Url
    date: date
    notify: bool


class ParseZamenaJsonRequest(BaseModel):
    file: str | UploadFile
    date: date


class RemoveZamenaRequest(BaseModel):
    date: date


class ParseZamenaV3Request(BaseModel):
    file: Optional[UploadFile]
    url: Optional[str]
    date: date
    
    
class ParseTeacherScheduleV3Request(BaseModel):
    file: UploadFile
    monday_date: date

class ParseZamenaV3Response(BaseModel):
    result: str