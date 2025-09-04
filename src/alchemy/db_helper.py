from asyncio import current_task
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.pool import NullPool  # <-- добавили

from src.core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # Lazy-init, чтобы не создавать engine/loop при импорте.
        self._url = url
        self._echo = echo
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    def _ensure_initialized(self) -> None:
        if self._engine is None:
            # КЛЮЧЕВОЕ: poolclass=NullPool исключает переиспользование коннектов между разными event loop’ами
            self._engine = create_async_engine(
                url=self._url,
                echo=self._echo,
                poolclass=NullPool,  # <-- важно
                future=True,
            )
            self._session_factory = async_sessionmaker(
                bind=self._engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )

    @property
    def engine(self) -> AsyncEngine:
        self._ensure_initialized()
        return self._engine  # type: ignore[return-value]

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        self._ensure_initialized()
        return self._session_factory  # type: ignore[return-value]

    def get_scoped_session(self):
        # Можно оставить, но обычно для async хватает session_factory()
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,  # type: ignore[arg-type]
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        self._ensure_initialized()
        async with self.session_factory() as session:  # type: ignore[call-arg]
            try:
                yield session
            finally:
                await session.close()

    async def dispose(self) -> None:
        """Явно закрыть движок, если нужно переинициализировать в этом же процессе."""
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None


# helpers
db_helper = DatabaseHelper(url=settings.db_url, echo=True)
local_db_helper = DatabaseHelper(url=settings.local_db, echo=True)
