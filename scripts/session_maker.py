from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from my_secrets import local_database_connection

engine: AsyncEngine = create_async_engine(local_database_connection, echo=True)

async_session_maker: sessionmaker[Session] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
