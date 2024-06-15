"""Landing models."""

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import (
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column


class LandingSettings(BigIntAuditBase):
    """Tag."""

    __tablename__ = "landing__settings"

    title: Mapped[str] = mapped_column(
        String(length=255), index=False, default="Ergostar"
    )
    footer_description: Mapped[str | None] = mapped_column(
        Text,
        index=False,
        default="Ergostar API provides a wide range of services to enhance your applications. From email and phone "
        "validation to VAT number validation, IP geolocation, WHOIS data, and advanced AI functionalities.",
    )
    footer_rights: Mapped[str] = mapped_column(
        Text, index=False, default="© 2024 Ergostar. All rights reserved."
    )

    url_login: Mapped[str] = mapped_column(
        String(length=255), index=False, default="/login/"
    )
    url_api_docs: Mapped[str] = mapped_column(
        String(length=255), index=False, default="/api/docs/"
    )
    url_register: Mapped[str] = mapped_column(
        String(length=255), index=False, default="/register/"
    )


class LandingHomePage(BigIntAuditBase):
    """Home page model."""

    __tablename__ = "landing__home_page"

    subtitle_1: Mapped[str | None] = mapped_column(
        String(length=255), index=False, default="Powerful & Versatile"
    )
    subtitle_2: Mapped[str | None] = mapped_column(
        String(length=255), index=False, default="API Services for Modern Applications"
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        index=False,
        default="Enhance your applications with Ergolon API's wide range of services, "
        "from email and phone validation to advanced AI functionalities. Seamlessly "
        "integrate our APIs to boost your app's performance and capabilities.",
    )
