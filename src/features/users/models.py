"""User model."""

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from src.features.auth.models import ApiKeyModel


class UserModel(BigIntAuditBase):
    """User model."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    api_keys: Mapped[list["ApiKeyModel"]] = relationship(
        "ApiKeyModel",
        back_populates="user",
    )
