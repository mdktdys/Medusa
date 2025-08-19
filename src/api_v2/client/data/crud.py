from typing import List

from src.alchemy.database import Groups
from src.alchemy.db_helper import AsyncSession
from src.api_v1.groups.crud import get_groups

from .schemas import FullDataDto


async def get_full_data(session: AsyncSession) -> FullDataDto:
    groups: List[Groups] = await get_groups(session = session)
    
    
    return FullDataDto(
        groups = groups
    )