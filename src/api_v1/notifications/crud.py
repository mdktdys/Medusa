from typing import List
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from src.api_v1.bench.schemas import Teacher
from src.firebase import fire


async def send_single_message(token: str, session: AsyncSession):
    response = fire.send_single_message(
        title='header',
        body='body',
        token=''
    )
    print(response)
    return response
