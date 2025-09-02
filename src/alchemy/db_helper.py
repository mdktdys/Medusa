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
        # internal storage for lazy-init objects
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    def _ensure_initialized(self) -> None:
        if self._engine is None:
            self._engine = create_async_engine(url=self._url, echo=self._echo)
            self._session_factory = async_sessionmaker(
                bind=self._engine, autoflush=False, autocommit=False, expire_on_commit=False
            )

    @property
    def engine(self) -> AsyncEngine:
        """Return AsyncEngine, initializing it if needed."""
        self._ensure_initialized()
        return self._engine  # type: ignore[return-value]

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Return async_sessionmaker, initializing it if needed."""
        self._ensure_initialized()
        return self._session_factory  # type: ignore[return-value]

    def get_scoped_session(self):
        # session_factory property ensures initialization
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task  # type: ignore[arg-type]
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """FastAPI dependency style async generator that yields an AsyncSession."""
        # session_factory property ensures initialization
        async with self.session_factory() as session:  # type: ignore[call-arg]
            try:
                yield session
            finally:
                await session.close()


# helpers
db_helper = DatabaseHelper(url=settings.db_url, echo=True)
local_db_helper = DatabaseHelper(url=settings.local_db, echo=True)

