"""Persistence models for the auth feature."""

from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from src.features.users.models import UserModel


class ApiKeyModel(UUIDv7AuditBase):
    """API key entity."""

    __tablename__ = "api_keys"

    key_hashed: Mapped[UUID] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="api_keys",
    )
