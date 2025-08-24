from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import db_helper
from src.api_v1.telegram_auth import crud
from src.api_v1.telegram_auth.schemas import CreateStateDto

router = APIRouter(tags=["telegram_auth"])

@router.post('/create_state', status_code = status.HTTP_201_CREATED)
async def create_state(session: AsyncSession = Depends(db_helper.session_dependency)) -> CreateStateDto:
    return await crud.create_state(session = session)