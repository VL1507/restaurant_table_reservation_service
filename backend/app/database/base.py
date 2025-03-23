from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.db1.base import BaseDB1, engin_db1
from app.database.db2.base import BaseDB2, engin_db2

async_session = async_sessionmaker(
    binds={BaseDB1: engin_db1, BaseDB2: engin_db2}, expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        return session
