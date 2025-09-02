import re
from typing import List, Sequence, Tuple

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.database_local import (
    Discipline,
    DisciplineCodes,
    EntityAlias,
    EntityKind,
    Group,
    LoadLink,
)
from src.utils import logger

NORMALIZE_RE: re.Pattern[str] = re.compile(r'[^a-zA-Zа-яА-Я0-9]+')

def _norm(s: str) -> str:
    return NORMALIZE_RE.sub('', s).lower()


async def find_group_disciplines_by_alias_or_name_or_code_discipline_name(
    session: AsyncSession,
    group: Group,
    raw: str,
    contains: bool = False,
) -> List[Discipline]:
    # Normalize query
    q: str = _norm(raw)
    if not q:
        return []

    results: List[Discipline] = []

    # First: search entity_aliases for discipline aliases
    alias_cond = EntityAlias.alias_normalized.ilike(f"%{q}%") if contains else (EntityAlias.alias_normalized == q)

    stmt_alias: Select[Tuple[int]] = (
        select(EntityAlias.entity_id)
        .where(
            EntityAlias.kind == EntityKind.DISCIPLINE.value,
            alias_cond,
        )
    )
    alias_rows: Sequence[int] = (await session.execute(stmt_alias)).scalars().all()

    if alias_rows:
        seen = set()
        ids = [i for i in alias_rows if not (i in seen or seen.add(i))]

        if ids:
            # only disciplines that are present in the group's load_linkers
            stmt_disc_by_ids: Select[Tuple[Discipline]] = (
                select(Discipline)
                .join(LoadLink, LoadLink.discipline_id == Discipline.id)
                .where(Discipline.id.in_(ids), LoadLink.group_id == group.id)
            )
            results = list((await session.execute(stmt_disc_by_ids)).scalars().all())

    # If alias search yielded nothing, fallback to name/code search
    if not results:
        # Normalize DB fields (remove non-alphanumeric and lower-case)
        disc_norm = func.lower(func.regexp_replace(Discipline.name, r'[^a-zA-Zа-яА-Я0-9]', '', 'g'))
        code_norm = func.lower(func.regexp_replace(DisciplineCodes.name, r'[^a-zA-Zа-яА-Я0-9]', '', 'g'))

        name_cond = disc_norm.ilike(f"%{q}%") if contains else (disc_norm == q)
        code_cond = code_norm.ilike(f"%{q}%") if contains else (code_norm == q)

        # only disciplines linked to this group; match either discipline.name or the linked discipline_code.name
        stmt_disc_by_name: Select[Tuple[Discipline]] = (
            select(Discipline)
            .join(LoadLink, LoadLink.discipline_id == Discipline.id)
            .outerjoin(DisciplineCodes, DisciplineCodes.id == LoadLink.discipline_code_id)
            .where(LoadLink.group_id == group.id)
            .where(name_cond | code_cond)
        )
        rows = (await session.execute(stmt_disc_by_name)).scalars().all()

        # dedupe and return
        seen_ids = set()
        for d in rows:
            if d is None:
                continue
            if d.id in seen_ids:
                continue
            seen_ids.add(d.id)
            results.append(d)

    return results


    # q: str = _norm(raw)
    # if not q:
    #     return []
    # logger.logger.info(q)
    # alias_cond = EntityAlias.alias_normalized.ilike(f"%{q}%") if contains else (EntityAlias.alias_normalized == q)

    # stmt_alias: Select[Tuple[int]] = (
    #     select(EntityAlias.entity_id)
    #     .where(
    #         EntityAlias.kind == EntityKind.DISCIPLINE.value,
    #         alias_cond,
    #     )
    # )
    # alias_rows: Sequence[int] = (await session.execute(stmt_alias)).scalars().all()
    # logger.logger.info(alias_rows)

    # results: list[Discipline] = []

    # if alias_rows:
    #     seen = set()
    #     ids = [i for i in alias_rows if not (i in seen or seen.add(i))]

    #     if ids:
    #         # only disciplines that are present in the group's load_linkers
    #         stmt_disc_by_ids: Select[Tuple[Discipline]] = (
    #             select(Discipline)
    #             .join(LoadLink, LoadLink.discipline_id == Discipline.id)
    #             .where(Discipline.id.in_(ids), LoadLink.group_id == group.id)
    #         )
    #         results = list((await session.execute(stmt_disc_by_ids)).scalars().all())

    # if not results:
    #     disc_norm = func.lower(func.regexp_replace(Discipline.name, r'[^a-zA-Zа-яА-Я0-9]', '', 'g'))
    #     code_norm = func.lower(func.regexp_replace(DisciplineCodes.name, r'[^a-zA-Zа-яА-Я0-9]', '', 'g'))

    #     name_cond = disc_norm.ilike(f"%{q}%") if contains else (disc_norm == q)
    #     code_cond = code_norm.ilike(f"%{q}%") if contains else (code_norm == q)

    #     # only disciplines linked to this group; match either discipline.name or the linked discipline_code.name
    #     stmt_disc_by_name: Select[Tuple[Discipline]] = (
    #         select(Discipline)
    #         .join(LoadLink, LoadLink.discipline_id == Discipline.id)
    #         .outerjoin(DisciplineCodes, DisciplineCodes.id == LoadLink.discipline_code_id)
    #         .where(LoadLink.group_id == group.id)
    #         .where(name_cond | code_cond)
    #     )
    #     results = list((await session.execute(stmt_disc_by_name)).scalars().all())

    # return results
