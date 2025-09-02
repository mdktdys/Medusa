from asyncio import current_task
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # Defer engine and session_factory creation until first use. This avoids
        # creating asyncio-related objects at import time (which can be created
        # in a different process or event loop when Celery forks) and then being
        # used on another loop — causing "Future attached to a different loop" errors.
        self._url = url
        self._echo = echo
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    def _ensure_initialized(self):
        if self.engine is None:
            self.engine = create_async_engine(url=self._url, echo=self._echo)
            self.session_factory = async_sessionmaker(
                bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
            )

    def get_scoped_session(self):
        self._ensure_initialized()
        # mypy: session_factory is Optional but ensured initialized above
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task  # type: ignore[arg-type]
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """FastAPI dependency style async generator that yields an AsyncSession."""
        self._ensure_initialized()
        # mypy: session_factory is Optional but ensured initialized above
        async with self.session_factory() as session:  # type: ignore[call-arg]
            yield session
            await session.close()


db_helper = DatabaseHelper(url=settings.db_url, echo = True)
local_db_helper = DatabaseHelper(url=settings.local_db, echo = True)

