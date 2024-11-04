import datetime

from pydantic import BaseModel


class ParseZamenaRequest(BaseModel):
    url: str
    date: datetime.datetime


class RemoveZamenaRequest(BaseModel):
    date: datetime.date
