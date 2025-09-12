from typing import Tuple

from fastapi_users.authentication import JWTStrategy
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.database_local import User
from src.utils.get_remote_file_bytes import get_remote_file_bytes_async

from .schemas import TelegramWebAppRequest, UserCreate
from .user_manager import UserManager


async def telegram_webapp_login(session: AsyncSession, request: TelegramWebAppRequest, jwt_strategy: JWTStrategy, user_manager: UserManager, refresh_strategy: JWTStrategy):
    telegram_id: str = str(request.user['id'])
    telegram_username: str | None = request.user.get('username')
    telegram_first_name: str | None = request.user.get('first_name')
    telegram_last_name: str | None = request.user.get('last_name')
    telegram_photo_url: str | None = request.user.get('photo_url')
    
    result: Result[Tuple[User]] = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user: User | None = result.scalar_one_or_none()
    
    photo_bytes: bytes | None
    if telegram_photo_url is not None:
        photo_bytes = await get_remote_file_bytes_async(telegram_photo_url)
    
    if user:
        updated: bool = False

        if telegram_username is not None and user.username != telegram_username:
            user.username = telegram_username
            updated = True
            
        if photo_bytes and user.photo_bytes != photo_bytes:
            user.photo_bytes = photo_bytes
            updated = True
            
        if updated:
            await session.commit()
            
            
    if user is None:
        pseudo_email: str = f"{telegram_id}@tg-login.uksivt.xyz"
        random_password = 'telegram_auth'

        user = await user_manager.create(
            UserCreate(
                email=pseudo_email,
                password=random_password,
                is_active=True,
                is_verified=True,
            )
        )
        user.telegram_id = telegram_id
        user.username = telegram_username
        user.first_name = telegram_first_name
        user.last_name = telegram_last_name
        user.photo_bytes = photo_bytes
        await session.commit()
        await session.refresh(user)

            
    access_token: str = await jwt_strategy.write_token(user)
    refresh_token: str = await refresh_strategy.write_token(user)

    return {
        'refresh_token': refresh_token,
        'access_token': access_token,
    }