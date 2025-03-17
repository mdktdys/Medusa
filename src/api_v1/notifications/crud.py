from sqlalchemy.ext.asyncio import AsyncSession
from src.firebase import fire
from src.parser.supabase import SupaBaseWorker


async def send_single_message(token: str, session: AsyncSession):
    response = fire.send_single_message(
        title='header',
        body='body',
        token=token
    )
    print(response)
    return response


async def send_message_to_all(title: str, body:str):
    sup = SupaBaseWorker()
    response = fire.send_message_to_topic(
        title=title,
        body=body,
        sup=sup
    )
    print(response)
    return response
