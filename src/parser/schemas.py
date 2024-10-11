import json
import base64
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class CheckResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str

    def to_dict(self):
        return self.dict()


class CheckResultError(CheckResult):
    error: str
    trace: str

    def to_dict(self):
        return self.dict()


class CheckZamenaResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str

    def to_dict(self):
        return self.dict()


class CheckZamenaResultFailed(CheckZamenaResult):
    result: str = "Failed"
    error: str
    trace: str

    def to_dict(self):
        return self.dict()


class CheckZamenaResultSuccess(CheckZamenaResult):
    result: str = "Success"
    link: str
    images: List[bytes]
    date: datetime.date

    def to_dict(self):
        # Convert images to base64 strings and date to ISO format
        return {
            "result": self.result,
            "link": self.link,
            "images": [base64.b64encode(img).decode("utf-8") for img in self.images],
            "date": self.date.isoformat(),
        }


class CheckResultFoundNew(CheckResult):
    checks: List[CheckZamenaResult] = []

    def to_dict(self):
        # Convert checks using their own `to_dict` method
        return {
            "result": self.result,
            "checks": [check.to_dict() for check in self.checks],
        }
