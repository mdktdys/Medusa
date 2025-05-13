from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import FirebaseSubscriber, FirebaseMessage
from src.firebase import fire
from src.parser.supabase import SupaBaseWorker


async def send_single_message(token: str, session: AsyncSession):
    response = fire.send_single_message(
        title='header',
        body='body',
        token=token
    )
    return response


async def send_message_to_all(title: str, body:str):
    sup = SupaBaseWorker()
    response = fire.send_message_to_topic(
        title=title,
        body=body,
        sup=sup
    )
    return response


async def send_multicast_message(message: FirebaseMessage, subscribers: List[FirebaseSubscriber]):
    fire.send_multicats_message(
        subscribers = subscribers,
        message = message,
    )


def get_firebase_item_subscribers(item_ids: list[int], item_type: int) -> List[FirebaseSubscriber]:
    sup = SupaBaseWorker()
    subscribers = (
        sup.client.table('MessagingClients')
        .select('token, clientID')
        .eq('subType', item_type)
        .in_('subID', item_ids)
        .execute()
    ).data

    return [FirebaseSubscriber(client_id = sub['clientID'], token = sub['token']) for sub in subscribers]
