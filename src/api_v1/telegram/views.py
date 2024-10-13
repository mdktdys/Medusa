from fastapi import APIRouter
from starlette import status

from src.api_v1.telegram import crud
from src.api_v1.telegram.schemas import Subscription

router = APIRouter(tags=["Telegram"])


@router.post("/subscribe_zamena_notifications")
async def subscribe_zamena_notifications(sub: Subscription):
    return await crud.subscribe_zamena_notifications(
        chat_id=sub.chat_id, target_id=sub.target_id, target_type=sub.target_type
    )


@router.post("/unsubscribe_zamena_notifications")
async def unsubscribe_zamena_notifications(sub: Subscription):
    return await crud.unsubscribe_zamena_notifications(
        chat_id=sub.chat_id, target_id=sub.target_id, target_type=sub.target_type
    )
