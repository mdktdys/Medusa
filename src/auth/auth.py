import uuid
from typing import List, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from my_secrets import API_KEY, PUBLIC_API_KEY, SECRET

# from src.alchemy.database import User
from src.alchemy.database_local import User
from src.alchemy.db_helper import local_db_helper

from .user_manager import UserManager

api_keys = [API_KEY, PUBLIC_API_KEY]


async def get_user_db(session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
    

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret = SECRET, lifetime_seconds=3600)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name = 'jwt',
    transport = bearer_transport,
    get_strategy = get_jwt_strategy,
)

def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret = SECRET, lifetime_seconds=30 * 24 * 3600)


def any_auth_method(roles: List[str]):
    async def dependency(
            api_key: Optional[str] = Depends(api_key_auth),
            user_id: User = Depends(current_active_user),
    ):
        if api_key:
            return True
        if user_id:
            if user_id.role in roles:
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No access",
                )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No valid authentication method found",
        )

    return dependency


async def api_key_auth(request: Request) -> bool:
    api_key: str | None = request.headers.get("X-API-KEY")
    if api_keys.__contains__(api_key):
        return True
    return False


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active = True, optional = True)
