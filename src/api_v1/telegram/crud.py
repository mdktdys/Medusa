import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Response, status

from src.parser.supabase import SupaBaseWorker

sup = SupaBaseWorker()


async def subscribe_zamena_notifications(
    chat_id: str, target_type: int, target_id: int, response: Response
):
    res = (
        sup.client.table("Subscribers")
        .select("id")
        .eq("chat_id", chat_id)
        .eq("chat_id", chat_id)
        .eq("target_type", target_type)
        .eq("target_id", target_id)
        .execute()
    )

    print(res.data)
    if len(res.data) > 0:
        response.status_code = status.HTTP_202_ACCEPTED
        return

    result = (
        sup.client.table("Subscribers")
        .insert(
            {"chat_id": chat_id, "target_type": target_type, "target_id": target_id}
        )
        .execute()
    )
    print(result)
    print(result.dict)
    response.status_code = status.HTTP_201_CREATED
    return


async def unsubscribe_zamena_notifications(
    chat_id: str, target_type: int, target_id: int, response: Response
):
    result = (
        sup.client.table("Subscribers")
        .delete()
        .eq("chat_id", chat_id)
        .eq("chat_id", chat_id)
        .eq("target_type", target_type)
        .eq("target_id", target_id)
        .execute()
    )
    print(result)
    print(result)
    response.status_code = status.HTTP_201_CREATED
    return


async def get_day_schedule_by_date(
    session: AsyncSession,
    chat_id: int,
    target_type: int,
    target_id: int,
    date: datetime.date,
):
    pass
