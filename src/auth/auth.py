from typing import Optional
from fastapi import Depends, FastAPI, Request
from fastapi_users import FastAPIUsers, schemas
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

from src.alchemy.database import Base
from src.alchemy.db_helper import local_db_helper
from src.auth.schemas import User, UserRead, UserCreate
from src.auth.users import fastapi_users, auth_backend

# Set your JWT secret and other constants
SECRET = "secret"
DATABASE_URL = "postgresql+asyncpg://root:banana@postgres:5432/Devotion"

router = APIRouter()


# Create the async engine and session maker
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Create the database and tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Set up the user database
async def get_user_db(
    session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    yield SQLAlchemyUserDatabase(session, User)


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


# Protected route example
@router.get("/protected-route", tags=["users"])
async def protected_route(
    user: User = Depends(fastapi_users.current_user(active=True)),
):
    return {"message": f"Hello {user.email}"}


# Run the database initialization at startup
@router.on_event("startup")
async def on_startup():
    await create_db_and_tables()
