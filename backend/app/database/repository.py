from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

Table = TypeVar(
    name="Table",
    # bound=Base
)


class Repository(Generic[Table]):
    table: type[Table]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, limit: int | None = None, offset: int | None = None):
        stmt = select(self.table).limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_by_id(self, id: int) -> type[Table] | None:
        stmt = select(self.table).where(self.table.id == id)  # type: ignore
        res = await self.session.scalar(stmt)
        return res  # type: ignore

    # FIXME
    # async def add_one(self, ) -> int:
    #     stmt = insert(self.table).values(kwargs).returning(self.table.id)
    #     res = await self.session.execute(stmt)
    #     await self.session.commit()
    #     return res.scalar_one()

    # async def del_one(self, id: int) -> None:
    #     try:
    #         instance = await self.session.scalar(
    #             select(self.model).where(self.model.id == id)
    #         )
    #         await self.session.delete(instance=instance)
    #         await self.session.commit()
    #     except Exception as e:
    #         logger.error(e)
    #         await self.session.rollback()
