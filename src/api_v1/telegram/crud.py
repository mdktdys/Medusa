import datetime
import locale
from typing import List
import httpx
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, Response, status

from src.api_v1.notifications.schemas import FirebaseMessage, FirebaseSubscriber
from src.api_v1.notifications.views import get_firebase_item_subscribers, send_multicast_message
from my_secrets import TELEGRAM_API_URL
from src.alchemy import database
from src.api_v1.groups.schemas import DayScheduleFormatted
from src.parser.supabase import SupaBaseWorker

sup = SupaBaseWorker()


async def get_chat_subscribers(
    session: AsyncSession, chat_id: int
) -> List[database.Subscribers]:
    query = select(database.Subscribers).where(database.Subscribers.chat_id == str(chat_id))
    result: Result = await session.execute(query)
    return list(result.scalars().all())
    
    
def get_teacher_subscribers(id: int)-> list[int]:
    return (
        sup.client.table('MessagingClients')
        .select('token, clientID')
        .eq('subType', 1)
        .eq('subID', id)
        .execute()
    ).data


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


async def telegram_send_message(chat_id: int, message: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TELEGRAM_API_URL + "/sendMessage", 
                json={
                    "chat_id": chat_id, 
                    "text": message,
                    "parse_mode": "HTML"
                },
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            response.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки сообщения: {str(e)}")


async def send_group_schedule_by_chat_id(chat_id: int, group_id: int, date: datetime.date, session: AsyncSession):
    from src.api_v1.groups.crud import get_group_day_schedule_by_date_formatted
    schedule_message_formatted: DayScheduleFormatted = await get_group_day_schedule_by_date_formatted(
        group_id=group_id,
        chat_id=chat_id,
        date=date,
        session=session,
    )
    message = f"🎓 Обнаружено изменение в расписании группы {schedule_message_formatted.search_name}\n"

    if len(schedule_message_formatted.paras) == 0:
        message += "\n🎉 Нет пар\n"

    if schedule_message_formatted.full_zamena:
        message += "🔴 Полное изменение расписания\n"

    for para in schedule_message_formatted.paras:
        message += f"{para}\n"

    message += f"\n📅 {date.strftime('%A').capitalize()}, {date.day} {date.strftime('%B')}"

    await telegram_send_message(chat_id, message)


async def notify_zamena(affected_groups: List[int], affected_teachers: List[int]):
    message = FirebaseMessage(
        title = 'Появились замены для тебя',
        body = 'В заменах есть изменения для тебя!' 
    )
    
    groups_subscribers: list[FirebaseSubscriber] = await get_firebase_item_subscribers(item_type = 1, item_ids = affected_groups)
    teachers_subscribers: list[FirebaseSubscriber] = await get_firebase_item_subscribers(item_type = 2, item_ids = affected_teachers)
    
    await send_multicast_message(
        subscribers = groups_subscribers + teachers_subscribers,
        message = message,
    )

    return None