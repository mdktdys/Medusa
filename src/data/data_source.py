import datetime

from src.models.holiday_model import Holiday
from src.models.zamena_full import ZamenaFull
from src.models.zamena_file_link_model import ZamenaFileLink
from src.models.zamenas import Zamenas
from src.models.paras_model import Paras
from src.models.lesson_timings_model import LessonTimings

class DataSource:
    async def load_timings(self) -> list[LessonTimings]:
        raise NotImplementedError

    async def get_lessons(
        self,
        group_id: int | None = None,
        teacher_id: int | None = None,
        cabinet_id: int | None = None,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[Paras]:
        raise NotImplementedError
    
    async def get_zamenas(
        self,
        group_id: int | None = None,
        teacher_id: int | None = None,
        cabinet_id: int | None = None,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[Zamenas]:
        raise NotImplementedError
    
    async def get_zamena_file_links(
        self,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[ZamenaFileLink]:
        raise NotImplementedError
    
    async def get_zamena_full(
        self,
        group_ids: list[int] | None = None,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[ZamenaFull]:
        raise NotImplementedError
    
    async def get_holidays(
        self,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[Holiday]:
        raise NotImplementedError