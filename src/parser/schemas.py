import datetime
from typing import List

from pydantic import BaseModel


class CheckResult(BaseModel):
    result: str


class CheckResultError(CheckResult):
    error: str
    trace: str


class CheckZamenaResult(BaseModel):
    result: str


class CheckZamenaResultFailed(CheckZamenaResult):
    result: str = "Failed"
    error: str
    trace: str


class CheckZamenaResultSuccess(CheckZamenaResult):
    result: str = "Success"
    link: str
    images: List[bytes]
    date: datetime.date


class CheckResultFoundNew(CheckResult):
    result: str
    checks: List[CheckZamenaResult] = []
