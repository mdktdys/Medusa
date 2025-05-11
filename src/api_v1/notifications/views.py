from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import FirebaseSubscriber, FirebaseMessage
from src.alchemy import db_helper
from src.api_v1.notifications import crud

router = APIRouter(tags=["Notifications"], include_in_schema=True)


@router.post("/send_single_message/")
async def send_single_message(token: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.send_single_message(session=session, token=token)


@router.post("/send_message_to_all/")
async def send_message_to_all(title: str, body: str):
    return await crud.send_message_to_all(title=title, body=body)


@router.post('/send_multicast_message')
async def send_multicast_message(message: FirebaseMessage, subscribers: List[FirebaseSubscriber]):
    return await crud.send_multicast_message(
        subscribers = subscribers,
        message = message,
    )


@router.get('/get_firebase_item_subscribers', response_model = List[FirebaseSubscriber])
async def get_firebase_item_subscribers(item_id: int, item_type: int) -> List[FirebaseSubscriber]:
    return crud.get_firebase_item_subscribers(
        item_id = item_id,
        item_type = item_type
    )