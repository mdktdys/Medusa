import datetime

from fastapi import UploadFile
from pydantic import BaseModel


class ParseZamenaRequest(BaseModel):
    url: str
    date: datetime.datetime
    notify: bool


class RemoveZamenaRequest(BaseModel):
    date: datetime.date
