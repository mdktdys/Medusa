from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import db_helper
from src.api_v1.telegram_auth import crud
from src.api_v1.telegram_auth.schemas import (AuthDto, AuthRequest,
                                              AuthStatusDto, AuthStatusRequest,
                                              CreateStateDto)
from src.auth.auth import any_auth_method

router = APIRouter(tags=["telegram_auth"])


@router.post('/create_state', status_code = status.HTTP_201_CREATED)
async def create_state(session: AsyncSession = Depends(db_helper.session_dependency)) -> CreateStateDto:
    return await crud.create_state(session = session)


@router.post("/auth_status")
async def auth_status(request: AuthStatusRequest, session: AsyncSession = Depends(db_helper.session_dependency)) -> AuthStatusDto | None:
    return await crud.auth_status(request = request, session = session)


@router.post('/verify_token', status_code = status.HTTP_201_CREATED, dependencies=[Depends(any_auth_method(roles=["Owner"]))])
async def verify_token(auth_request: AuthRequest, session: AsyncSession = Depends(db_helper.session_dependency)) -> AuthDto:
    return await crud.verify_token(session = session, auth_request = auth_request)
