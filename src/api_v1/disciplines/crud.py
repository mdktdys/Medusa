import re
from typing import List, Sequence, Tuple

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.database_local import Discipline, EntityAlias, EntityKind
from src.utils import logger

NORMALIZE_RE: re.Pattern[str] = re.compile(r'[^a-zA-Zа-яА-Я0-9]+')

def _norm(s: str) -> str:
    return NORMALIZE_RE.sub('', s).lower()


async def find_disciplines_by_alias_or_name(
    session: AsyncSession,
    raw: str,
    contains: bool = True,
) -> List[Discipline]:
    q: str = _norm(raw)
    if not q:
        return []
    logger.logger.info(q)
    alias_cond = EntityAlias.alias_normalized.ilike(f"%{q}%") if contains else (EntityAlias.alias_normalized == q)

    stmt_alias = (
        select(EntityAlias.entity_id)
        .where(
            EntityAlias.kind == EntityKind.DISCIPLINE,
            alias_cond,
        )
    )
    alias_rows: Sequence[int] = (await session.execute(stmt_alias)).scalars().all()
    logger.logger.info(alias_rows)

    results: list[Discipline] = []

    if alias_rows:
        seen = set()
        ids = [i for i in alias_rows if not (i in seen or seen.add(i))]

        if ids:
            stmt_disc_by_ids: Select[Tuple[Discipline]] = select(Discipline).where(Discipline.id.in_(ids))
            results = list((await session.execute(stmt_disc_by_ids)).scalars().all())

    if not results:
        disc_norm = func.lower(func.regexp_replace(Discipline.name, r'[^a-zA-Zа-яА-Я0-9]', '', 'g'))
        name_cond = disc_norm.ilike(f"%{q}%") if contains else (disc_norm == q)

        stmt_disc_by_name: Select[Tuple[Discipline]] = select(Discipline).where(name_cond)
        results = list((await session.execute(stmt_disc_by_name)).scalars().all())

    return results
