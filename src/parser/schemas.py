import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class CheckResult(BaseModel):
    model_config = ConfigDict(from_attributes=True, ser_json_bytes="base64")
    result: str


class CheckResultError(CheckResult):
    error: str
    trace: str


class CheckZamenaResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str


class CheckZamenaResultFailed(CheckZamenaResult):
    result: str = "Failed"
    error: str
    trace: str


class CheckZamenaResultSuccess(CheckZamenaResult):
    result: str = "Success"
    link: str
    images: List[bytes]
    # date: datetime.date


class CheckResultFoundNew(CheckResult):
    checks: List[CheckZamenaResult] = []
