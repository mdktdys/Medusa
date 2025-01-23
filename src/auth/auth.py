from fastapi import APIRouter, HTTPException, Depends, Request, status

from my_secrets import SECRET, API_KEY, IS_DEV, PUBLIC_API_KEY
from src.auth.schemas import UserRead, UserCreate
import uuid
from typing import Optional, List
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy.db_helper import local_db_helper
from src.auth.schemas import User

router = APIRouter()
api_keys = [API_KEY, PUBLIC_API_KEY]


# Функция для проверки API ключа
async def api_key_auth(request: Request) -> bool:
    api_key = request.headers.get("X-API-KEY")
    if api_keys.__contains__(api_key):
        return True
    return False


# Получение базы данных пользователей
async def get_user_db(
        session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    yield SQLAlchemyUserDatabase(session, User)


# Менеджер пользователей
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])


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


current_active_user = fastapi_users.current_user(active=True, optional=True)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    dependencies=[Depends(any_auth_method(roles=["Owner"]))],
    tags=["Auth"],
)


@router.get(
    "/protected-route",
    tags=["Users"],
    dependencies=[Depends(any_auth_method(roles=["Owner"]))],
    include_in_schema=IS_DEV,
)
async def protected_route():
    return {"message": "Hello, you have access to the protected route!"}
