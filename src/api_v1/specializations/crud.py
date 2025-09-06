from typing import List, Sequence, Tuple

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.database_local import Specialization

from .schemas import SpecializationDto, SpecializationsResponse


async def get_specializations(session: AsyncSession) -> SpecializationsResponse:
    query: Select[Tuple[Specialization]] = select(Specialization).order_by(Specialization.name)
    specializations_raw: Sequence[Specialization] = (await session.execute(query)).scalars().all()
    specializations: List[SpecializationDto] = [
        SpecializationDto(
            id = spec.id,
            name = spec.name,
            code = spec.code,
        )

        for spec in specializations_raw
    ]
    return SpecializationsResponse(specialization = specializations)
