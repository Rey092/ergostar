"""Persistence models for the auth feature."""

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine

from src.config import settings
from src.features.users.models import UserModel


class ApiKeyModel(BigIntAuditBase):
    """API key entity."""

    __tablename__ = "api_keys"

    key: Mapped[str] = mapped_column(
        StringEncryptedType(
            Unicode,
            settings.app.SECRET_KEY,
            FernetEngine,
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
