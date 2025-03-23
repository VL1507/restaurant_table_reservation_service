from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.utils.custom_logger import setup_logger

logger = setup_logger(__name__)


class UnitOfWork:
    session_factory: async_sessionmaker[AsyncSession]
    session: AsyncSession

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self.session_factory = session_factory

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    @asynccontextmanager
    async def start_with(self):
        self.session = self.session_factory()
        try:
            yield self
            await self.commit()
        except Exception as e:
            logger.exception(e)
            await self.rollback()
