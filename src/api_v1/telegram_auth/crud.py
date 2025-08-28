import uuid
from typing import Tuple

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi_users.authentication import JWTStrategy
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database_local
from src.auth.auth import get_jwt_strategy, get_refresh_jwt_strategy

from .schemas import (
    AuthDto,
    AuthRequest,
    AuthStatusDto,
    AuthStatusRequest,
    CreateStateDto,
)


async def create_state(session: AsyncSession) -> CreateStateDto:
    token: str = str(uuid.uuid4())
    session.add(database_local.TelegramAuthState(token = token))
    await session.commit()
    return CreateStateDto(token = token)


async def auth_status(request: AuthStatusRequest, session: AsyncSession) -> AuthStatusDto | None:
    result: Result[Tuple[database_local.TelegramAuthState]] = await session.execute(select(database_local.TelegramAuthState).where(database_local.TelegramAuthState.token == request.token))
    state: database_local.TelegramAuthState | None = result.scalars().first()

    if state is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    if state.access_token is None or state.refresh_token is None:
        raise HTTPException(status_code = status.HTTP_202_ACCEPTED, detail = 'token not binded')

    await session.delete(state)
    await session.commit()
    return AuthStatusDto(
        access_token = state.access_token,
        refresh_token = state.refresh_token
    )
    

async def verify_token(session: AsyncSession, auth_request: AuthRequest) -> AuthDto:
    auth_state: Result[Tuple[database_local.TelegramAuthState]] = await session.execute(select(database_local.TelegramAuthState).where(database_local.TelegramAuthState.token == auth_request.token))
    state: database_local.TelegramAuthState | None = auth_state.scalars().first()

    if not state:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Token not found'
        )
    
    result: Result[Tuple[database_local.User]] = await session.execute(select(database_local.User).where(database_local.User.chat_id == auth_request.chat_id))
    user: database_local.User | None = result.scalars().first()
    
    if not user:
        new_user = database_local.User(
            chat_id = auth_request.chat_id,
            photo_url = auth_request.photo_bytes,
            username = auth_request.username,
            first_name = auth_request.first_name,
            last_name = auth_request.last_name,
            telegram_id = auth_request.user_id,
            hashed_password = "telegram_auth",
            email = f"{auth_request.chat_id}@telegram.local",
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        user = new_user

    access_strategy: JWTStrategy = get_jwt_strategy()
    refresh_strategy: JWTStrategy = get_refresh_jwt_strategy()

    access_token: str = await access_strategy.write_token(user)
    refresh_token: str = await refresh_strategy.write_token(user)

    state.access_token = access_token
    state.refresh_token = refresh_token
    await session.commit()

    return AuthDto(result = 'ok')