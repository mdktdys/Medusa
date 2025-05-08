import datetime

from pydantic import BaseModel
from pydantic_core import Url


class ParseZamenaRequest(BaseModel):
    url: Url
    date: datetime.date
    notify: bool


class RemoveZamenaRequest(BaseModel):
    date: datetime.date
