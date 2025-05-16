import datetime
from src.models.lesson_timings_model import LessonTimings
from src.models.holiday_model import Holiday
from my_secrets import SUPABASE_SECRET_KEY, SUPABASE_URL
from src.models.zamena_file_link_model import ZamenaFileLink
from src.models.zamenas import Zamenas
from src.models.zamena_full import ZamenaFull
from .data_source import DataSource
from src.models.paras_model import Paras
from supabase import AsyncClient, acreate_client

class SupabaseDataSource(DataSource):
    async def __init__(self):
        self.supabase: AsyncClient = await acreate_client(
            supabase_key = SUPABASE_SECRET_KEY,
            supabase_url = SUPABASE_URL,
        )
        await super().__init__()
        
        
    async def load_timings(self) -> list[LessonTimings]:
        result = await self.supabase.from_('timings').select('*').execute()
        return [LessonTimings.fromMap(data) for data in result.data]

    async def get_lessons(
        self,
        group_id: int | None = None,
        teacher_id: int | None = None,
        cabinet_id: int | None = None,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[Paras]:
        query = self.supabase.from_('Paras').select('*')

        if group_id is not None:
            query = query.eq('group', group_id)
        if teacher_id is not None:
            query = query.eq('teacher', teacher_id)
        if cabinet_id is not None:
            query = query.eq('cabinet', cabinet_id)
        if date_from is not None:
            query = query.gte('date', date_from.isoformat())
        if date_to is not None:
            query = query.lte('date', date_to.isoformat())

        result = await query.execute()
        return [Paras.fromMap(data) for data in result.data]
    
    
    async def get_zamenas(
        self,
        group_id: int | None = None,
        teacher_id: int | None = None,
        cabinet_id: int | None = None,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[Zamenas]:
        query = self.supabase.from_('Zamenas').select('*')

        if group_id is not None:
            query = query.eq('group', group_id)
        if teacher_id is not None:
            query = query.eq('teacher', teacher_id)
        if cabinet_id is not None:
            query = query.eq('cabinet', cabinet_id)
        if date_from is not None:
            query = query.gte('date', date_from.isoformat())
        if date_to is not None:
            query = query.lte('date', date_to.isoformat())

        result = await query.execute()
        return [Zamenas.fromMap(data) for data in result.data]
    
    
    async def get_zamena_file_links(
        self,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[ZamenaFileLink]:
        query = self.supabase.from_('ZamenaFileLinks').select('*')
        
        if date_from is not None:
            query = query.gte('date', date_from)
        if date_to is not None:
            query = query.lte('date', date_to)
        
        result = await query.execute()
        return [ZamenaFileLink.fromMap(data) for data in result.data]
    
    
    async def get_zamena_full(
        self,
        group_ids: list[int] | None = None,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[ZamenaFull]:
        query = self.supabase.from_('ZamenasFull').select('*')
        
        if group_ids is not None:
            query = query.in_('group', group_ids)
        if date_from is not None:
            query = query.gte('date', date_from)
        if date_to is not None:
            query = query.lte('date', date_to)
            
        result = await query.execute()
        return [ZamenaFull.fromMap(data) for data in result.data]
    
    
    async def get_holidays(
        self,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
    ) -> list[Holiday]:
        query = self.supabase.from_('Holidays').select('*')
        
        if date_from is not None:
            query = query.gte('date', date_from)
        if date_to is not None:
            query = query.lte('date', date_to)
            
        result = await query.execute()
        return [Holiday.fromMap(data) for data in result.data]
        
         
         
         