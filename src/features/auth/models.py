"""Persistence models for the auth feature."""

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from src.config import settings

if TYPE_CHECKING:
    from src.features.users.models import UserModel


class ApiKeyModel(BigIntAuditBase):
    """API key entity."""

    __tablename__ = "api_keys"

    key: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.app.SECRET_KEY,
            AesEngine,
            "pkcs5",
        ),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="api_keys",
    )
