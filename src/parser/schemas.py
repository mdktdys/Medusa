import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class CheckResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str


class CheckResultError(CheckResult):
    model_config = ConfigDict(from_attributes=True)
    error: str
    trace: str


class CheckZamenaResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str


class CheckZamenaResultFailed(CheckZamenaResult):
    model_config = ConfigDict(from_attributes=True)
    result: str = "Failed"
    error: str
    trace: str


class CheckZamenaResultSuccess(CheckZamenaResult):
    model_config = ConfigDict(from_attributes=True)
    result: str = "Success"
    link: str
    images: List[bytes]
    date: datetime.date


class CheckResultFoundNew(CheckResult):
    model_config = ConfigDict(from_attributes=True)
    result: str
    checks: List[CheckZamenaResult] = []
