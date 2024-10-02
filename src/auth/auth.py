from functools import partial, wraps
from typing import Optional, List
from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi_users import FastAPIUsers, schemas, jwt
from fastapi_users.authentication import (
    JWTStrategy,
    AuthenticationBackend,
    BearerTransport,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from src.alchemy.database import Base
from src.alchemy.db_helper import local_db_helper
from src.auth.schemas import User, UserRead, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator
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

# Set your JWT secret and other constants
SECRET = "SECRET"

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

ROLES = {"admin": []}


def authorize(roles):

    def decorator(func):
        async def wrapper(current_user: User = Depends(current_active_user)):
            if current_user.role not in roles:
                raise HTTPException(status_code=403, detail="Unauthorized")
            return await func()

        return wrapper

    return decorator


@router.get("/protected-route", tags=["users"])
@authorize(roles=["owner"])
async def protected_route():
    return {"message": f"Hello "}
