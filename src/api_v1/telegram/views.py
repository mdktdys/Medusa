import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import db_helper
from src.api_v1.telegram import crud
from src.api_v1.telegram.schemas import AuthRequest, DaySchedule, Subscription

router = APIRouter(tags=["Telegram"])


@router.post('/verify', status_code = status.HTTP_201_CREATED)
async def verify_token(auth_request: AuthRequest, session: AsyncSession = Depends(db_helper.session_dependency)) -> None:
    return await crud.verify_token(session = session, auth_request = auth_request)


@router.post("/subscribe_zamena_notifications")
async def subscribe_zamena_notifications(sub: Subscription, response: Response):
    return await crud.subscribe_zamena_notifications(
        chat_id=sub.chat_id,
        target_id=sub.target_id,
        target_type=sub.target_type,
        response=response,
    )


@router.post("/unsubscribe_zamena_notifications")
async def unsubscribe_zamena_notifications(sub: Subscription, response: Response):
    return await crud.unsubscribe_zamena_notifications(
        chat_id=sub.chat_id,
        target_id=sub.target_id,
        target_type=sub.target_type,
        response=response,
    )


@router.get(
    "/day_schedule/{target_type}/{target_id}/{date}/{chat_id}/",
    response_model=DaySchedule,
)
@cache(expire=6000)
async def get_day_schedule_by_date(
    target_id: int,
    target_type: int,
    chat_id: int,
    date: datetime.date,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> DaySchedule:
    return await crud.get_day_schedule_by_date(
        session=session,
        target_type=target_type,
        target_id=target_id,
        date=date,
        chat_id=chat_id,
    )


@router.post("/send_group_schedule_by_chat_id")
async def send_group_schedule_by_chat_id(chat_id: int, group_id: int, date: datetime.date, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.send_group_schedule_by_chat_id(chat_id=chat_id, group_id=group_id, date=date, session=session)


@router.post('/notify_zamena')
async def notify_zamena(affected_groups: List[int], affected_teachers: List[int]):
    return await crud.notify_zamena(affected_groups = affected_groups, affected_teachers = affected_teachers)

