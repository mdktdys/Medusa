from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import db_helper
from src.api_v1.notifications import crud

router = APIRouter(tags=["Notifications"], include_in_schema=True)


@router.post("/send_single_message/")
async def send_single_message(token: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.send_single_message(session=session, token=token)
