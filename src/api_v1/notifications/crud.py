from sqlalchemy.ext.asyncio import AsyncSession
from src.firebase import fire


async def send_single_message(token: str, session: AsyncSession):
    response = fire.send_single_message(
        title='header',
        body='body',
        token=token
    )
    print(response)
    return response
