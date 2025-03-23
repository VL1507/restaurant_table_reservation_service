import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column


class BaseMixin:
    pass


class IntegerIDMixin(BaseMixin):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        sort_order=-100,
    )


class UUID4Mixin(BaseMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        sort_order=-100,
    )


def datetime_utc() -> datetime:
    return (
        datetime.now(timezone.utc)
        # .replace(tzinfo=None)
    )


class TimestampMixin(BaseMixin):
    created_at: Mapped[datetime] = mapped_column(
        default=datetime_utc,
        sort_order=100,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime_utc,
        onupdate=datetime_utc,
        sort_order=101,
    )
