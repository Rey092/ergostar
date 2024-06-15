"""Landing models."""

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column


class LandingSettings(BigIntAuditBase):
    """Tag."""

    __tablename__ = "landing__settings"
    title: Mapped[str] = mapped_column(index=False)
    footer_description: Mapped[str | None] = mapped_column(
        String, index=False, nullable=True
    )
    footer_rights: Mapped[str] = mapped_column(index=False)

    url_login: Mapped[str] = mapped_column(index=False)
    url_api_docs: Mapped[str] = mapped_column(index=False)
    url_register: Mapped[str] = mapped_column(index=False)


class HomePage(BigIntAuditBase):
    """Home page model."""

    __tablename__ = "landing__home_page"

    subtitle_1: Mapped[str | None] = mapped_column(
        String(length=255), index=False, nullable=True
    )
    subtitle_2: Mapped[str | None] = mapped_column(
        String(length=255), index=False, nullable=True
    )
    description: Mapped[str | None] = mapped_column(String, index=False, nullable=True)
