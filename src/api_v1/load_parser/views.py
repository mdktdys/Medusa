import asyncio
from io import BytesIO
from typing import List

from fastapi import APIRouter, Depends

from src.alchemy.db_helper import AsyncSession, local_db_helper
from src.api_v1.groups.schemas import CreateGroupRequest
from src.api_v1.groups.views import create_group

from . import crud

router = APIRouter(tags=["ParseLoad"])


@router.post("/parse_load")
async def parse_load(session: AsyncSession = Depends(local_db_helper.session_dependency)):
    file_name = 'scripts/load_parsers/Нагрузка на 2025-2026 уч год.xlsx'
    with open(file_name, 'rb') as f:
        data: bytes = f.read()               
    bytes_ = BytesIO(data)

    result: List[tuple[str, str, int, int, int]] = await crud.parse_load_from_excel(bytes_ = bytes_)
    
    for raw_group in result:
        request = CreateGroupRequest(
            name = raw_group[0],
            commerce = raw_group[1] == 'к',
            department_id = raw_group[2],
            specialization_id = raw_group[3],
            course = raw_group[4],
        )
        await create_group(
            request = request,
            session = session
        )
        
        await asyncio.sleep(1)
    


