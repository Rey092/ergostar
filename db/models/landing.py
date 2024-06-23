"""Landing models."""

from advanced_alchemy.base import BigIntAuditBase
from fastapi_storages import FileSystemStorage
from fastapi_storages import StorageFile
from fastapi_storages.integrations.sqlalchemy import FileType
from litestar.datastructures import UploadFile
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.landing.enums import LandingSnippetLanguage


class LandingSettings(BigIntAuditBase):
    """Tag."""

    __tablename__ = "landing__settings"

    title: Mapped[str] = mapped_column(
        String(length=255), index=False, default="Ergostar"
    )
    footer_description: Mapped[str | None] = mapped_column(
        Text,
        index=False,
        default="Ergostar API provides a wide range of services to "
        "enhance your applications. From email and phone "
        "validation to VAT number validation, IP geolocation,"
        " WHOIS data, and advanced AI functionalities.",
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


class LandingSolution(BigIntAuditBase):
    """Landing service model."""

    __tablename__ = "landing__solution"

    title: Mapped[str] = mapped_column(String(length=255), index=False)
    title_carousel: Mapped[str] = mapped_column(String(length=255), index=False)
    description: Mapped[str] = mapped_column(Text, index=False)
    is_top_active: Mapped[bool] = mapped_column(Boolean, index=True, default=True)
    is_carousel_active: Mapped[bool] = mapped_column(Boolean, index=True, default=True)
    docs_url: Mapped[str] = mapped_column(
        String(length=255), index=False, default="https://google.com"
    )
    file: Mapped[StorageFile | UploadFile] = Column(  # type: ignore
        FileType(storage=FileSystemStorage(path="./media")), default=""
    )


class LandingSnippet(BigIntAuditBase):
    """Landing snippet model."""

    __tablename__ = "landing__snippet"

    tab: Mapped[str] = mapped_column(String(length=255), index=False)
    title: Mapped[str] = mapped_column(String(length=255), index=False)
    subtitle: Mapped[str] = mapped_column(String(length=255), index=False)
    description: Mapped[str] = mapped_column(Text, index=False)
    is_active: Mapped[bool] = mapped_column(Boolean, index=True, default=True)
    code: Mapped[str] = mapped_column(Text, index=False)
    code_language: Mapped[LandingSnippetLanguage] = mapped_column(
        String(length=20),
        index=False,
    )
    feather_icon: Mapped[str] = mapped_column(
        String(length=40), index=False, default="test", nullable=True
    )

    # type_annotation_map = {
    #     LandingSnippetLanguage: sqlalchemy.Enum
    #     (LandingSnippetLanguage, length=20, native_enum=False)
    # }
