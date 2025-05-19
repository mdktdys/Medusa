from typing import List
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from src.api_v1.bench.schemas import Teacher
import requests
import json
from my_secrets import OPENROUTER_API_KEY

async def bench_alchemy(session: AsyncSession) -> List[Teacher]:
    query = select(database.Teachers)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def bench_supabase(session: AsyncSession, supabase) -> List[Teacher]:
    data, _ = supabase.table("Teachers").select("*").execute()
    return [Teacher.parse_obj(x) for x in data[1]]


promt: str = 'Напиши списком через запятую группы которые на практике. Учти, что запись  21СА-1,2 это имеется ввиду 21СА-1 и 21СА-2. Перечисли через запятую все группы, не пиши ничего лишнего кроме групп'
test: str = '''
Зам.директора по учебной работе
________________З.З. Курмашева
«_______» _____________ 2025 года
КОРРЕКТИРОВКА РАСПИСАНИЯ
НА 19 МАЯ – ПОНЕДЕЛЬНИК
Группы: 23уЛ-1; 22ЗИО-1,2; 22Л-1,2; 22ПО-1,2,3; 22ПСА-1,2,3; 22уКСК-1; 22Э-1,2; 21БД-1; 21ВЕБ-1,2;
21ИС-1; 21ОИБ-1,2; 21П-1,2; 21СА-1,2 – на производственной практике
Замена кабинетов:
'''


def send_ai_request():
    response: requests.Response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    },
    data = json.dumps({
        "model": "openai/gpt-4o", # Optional
        "messages": [
        {
            "role": "user",
            "content": f"{promt}\n{test}"
        }
        ]
    })
    )
    print(response)
    print(response.json())
    return response.json()