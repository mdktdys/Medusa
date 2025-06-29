import datetime
from typing import List, Tuple

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
    result: str = "ok"
    liquidation_groups: list[int]
    full_zamena_groups: list[int]
    practice_groups: list[int]
    zamenas: list[dict]
    teacher_cabinet_switches: list[Tuple[int, int]]
    file_hash: str
    date: datetime.date
    url: str