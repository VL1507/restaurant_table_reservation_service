from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.mixins import IntegerIDMixin, TimestampMixin

from .base import BaseDB1
