from fastapi import APIRouter
from fastapi import HTTPException

from my_secrets import SECRET
from src.auth.schemas import UserRead, UserCreate
import uuid
from typing import Optional

from fastapi import Depends, Request
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


async def get_user_db(
    session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    yield SQLAlchemyUserDatabase(session, User)


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
current_active_user = fastapi_users.current_user(active=True)


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)


def authorize(roles):
    def decorator(func):
        async def wrapper(
            request: Request,
            current_user: Optional[User] = Depends(current_active_user),
        ):
            trusted_services = ["telegram_bot"]
            if request.headers.get("X-Internal-Service-Name") in trusted_services:
                return await func()

            if current_user.role not in roles:
                raise HTTPException(status_code=403, detail="Unauthorized")

            return await func()

        return wrapper

    return decorator


@router.get("/protected-route", tags=["Users"])
@authorize(roles=["Owner"])
async def protected_route():
    return {"message": f"Hello "}
