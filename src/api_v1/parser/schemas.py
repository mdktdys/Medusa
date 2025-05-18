import datetime

from fastapi import UploadFile
from pydantic import BaseModel
from pydantic_core import Url


class ParseZamenaRequest(BaseModel):
    url: Url
    date: datetime.date
    notify: bool


class ParseZamenaJsonRequest(BaseModel):
    file: str | UploadFile
    date: datetime.date


class RemoveZamenaRequest(BaseModel):
    date: datetime.date
