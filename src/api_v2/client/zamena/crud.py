import asyncio

from .schemas import ZamenaRequest, ZamenaResponse
from src.alchemy.db_helper import AsyncSession
from src.api_v1.zamenas.crud import get_zamenas
from src.api_v1.zamenas.schemas import ZamenaFilter
from src.api_v1.zamenas_full.crud import get_zamenas_full
from src.api_v1.zamenas_full.schemas import ZamenasFullFilter
from src.api_v1.zamena_file_links.schemas import ZamenaFileLinksFilter
from src.api_v1.zamena_file_links.crud import get_zamena_file_links

async def get_zamena(request: ZamenaRequest, session: AsyncSession) -> ZamenaResponse:
    zamena_filter = ZamenaFilter(start_date = request.date_to, end_date = request.date_from)
    zamena_filter_full = ZamenasFullFilter(group = [], date_from = request.date_from, date_to = request.date_to)
    zamena_file_links = ZamenaFileLinksFilter(start_date = request.date_to, end_date = request.date_from)

    zamenas, zamenas_full, zamena_file_links = await asyncio.gather(
        get_zamenas(session=session, filter = zamena_filter),
        get_zamenas_full(session = session, filter = zamena_filter_full),
        get_zamena_file_links(session = session, filter = zamena_file_links)
        # get_practices(session = session),
    )
    
    return ZamenaResponse(
        zamenas = zamenas,
        zamenas_full = zamenas_full,
        zamena_file_links = zamena_file_links,
        practices = [],
        cabinet_swaps = [],
    )