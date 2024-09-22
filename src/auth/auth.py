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

# Set your JWT secret and other constants
SECRET = "secret"
DATABASE_URL = "postgresql+asyncpg://root:banana@postgres:5432/Devotion"

router = APIRouter()


# Base model
class Base(DeclarativeBase):
    pass


class UserRead(schemas.BaseUser[UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


# User model (inherits from BaseUser)
class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


# Create the async engine and session maker
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Create the database and tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dependency to get async session
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


# Set up the user database
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# User Manager
class UserManager(BaseUserManager[User, UUID]):
    user_db_model = User

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# JWT Strategy for token generation
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# Authentication backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="jwt/login"),
    get_strategy=get_jwt_strategy,
)

# FastAPI Users object
fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

# Include the routes for user authentication and registration
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
