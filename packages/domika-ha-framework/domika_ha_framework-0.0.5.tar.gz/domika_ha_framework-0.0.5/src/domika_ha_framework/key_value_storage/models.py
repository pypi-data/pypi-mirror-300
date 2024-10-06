# vim: set fileencoding=utf-8
"""
Application key-value storage.

(c) DevPocket, 2024


Author(s): Michael Bogorad
"""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin
from sqlalchemy.orm import Mapped, mapped_column

from ..models import AsyncBase


class KeyValue(AsyncBase):
    """Application key-value storage."""

    __tablename__ = 'key_value'

    user_id: Mapped[str] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]


@dataclass
class DomikaKeyValueBase(DataClassJSONMixin):
    """Base key-value model."""

    user_id: str
    key: str
    value: str


@dataclass
class DomikaKeyValueCreate(DomikaKeyValueBase):
    """Key-value create model."""


@dataclass
class DomikaKeyValueRead(DomikaKeyValueBase):
    """Key-value read model."""

