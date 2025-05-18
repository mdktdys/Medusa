from typing import List

from pydantic import BaseModel, ConfigDict


class ZamenaParseResult(BaseModel):
    model_config = ConfigDict()
    result: str


class ZamenaParseFailed(ZamenaParseResult):
    error: str
    trace: str


class ZamenaParseFailedNotFoundItems(ZamenaParseFailed):
    items: List[str]


class ZamenaParseSucess(ZamenaParseResult):
    result: str = "ok"
    affected_teachers: List[int]
    affected_groups: List[int]

class ZamenaParseResultJson(ZamenaParseResult):
    test: str