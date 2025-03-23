from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class BaseDB1(AsyncAttrs, DeclarativeBase): ...


engin_db1 = create_async_engine(settings.db.db1_url, echo=settings.db.db_echo)
