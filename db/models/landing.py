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

    subtitle_1: Mapped[str] = mapped_column(
        String(length=255), index=False, default="Powerful & Versatile"
    )
    subtitle_2: Mapped[str] = mapped_column(
        String(length=255), index=False, default="API Services for Modern Applications"
    )
    description: Mapped[str] = mapped_column(
        Text,
        index=False,
        default="Enhance your applications with Ergolon API's wide range of services, "
        "from email and phone validation to advanced AI functionalities. Seamlessly "
        "integrate our APIs to boost your app's performance and capabilities.",
    )

    you_get_label: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default="Futures", nullable=False
    )

    you_get_title: Mapped[str] = mapped_column(
        String(length=255),
        index=False,
        server_default="What you will get with Ergostar API",
    )

    you_get_subtitle: Mapped[str | None] = mapped_column(
        String(length=255),
        index=False,
        server_default="Our API services are designed to help "
        "you build powerful and versatile applications.",
    )

    you_get_block_1_title: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default="Dashboard"
    )

    you_get_block_1_description: Mapped[str] = mapped_column(
        Text,
        index=False,
        server_default="Get a bird's eye view of your "
        "account and manage your API keys, "
        "usage, and billing information.",
    )

    you_get_block_1_feather_icon: Mapped[str] = mapped_column(
        String(length=40), index=False, server_default="pie-chart"
    )

    you_get_block_2_title: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default="Save money"
    )

    you_get_block_2_description: Mapped[str] = mapped_column(
        Text,
        index=False,
        server_default="Save money by using our versatile range of API services.",
    )

    you_get_block_2_feather_icon: Mapped[str] = mapped_column(
        String(length=40), index=False, server_default="dollar-sign"
    )

    you_get_block_3_title: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default="Boost Performance"
    )

    you_get_block_3_description: Mapped[str] = mapped_column(
        Text,
        index=False,
        server_default="Boost your app's performance "
        "and capabilities by integrating our APIs.",
    )

    you_get_block_3_feather_icon: Mapped[str] = mapped_column(
        String(length=40), index=False, server_default="trending-up"
    )

    you_get_block_4_title: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default="Documentation"
    )

    you_get_block_4_description: Mapped[str] = mapped_column(
        Text,
        index=False,
        server_default="Access our comprehensive documentation to "
        "learn more about our API services.",
    )

    you_get_block_4_feather_icon: Mapped[str] = mapped_column(
        String(length=40), index=False, server_default="book"
    )

    get_started_label: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default="Get Started"
    )

    get_started_title: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default="Ergolon saves"
    )

    get_started_array: Mapped[str] = mapped_column(
        String(length=255), index=False, server_default='"Time", "Money", "Effort"'
    )

    get_started_description: Mapped[str | None] = mapped_column(
        Text,
        index=False,
        server_default="Ergolon API saves you tons of hard work and time by providing "
        "you with a wide range of services to enhance your applications.",
    )

    get_started_lower_title: Mapped[str | None] = mapped_column(
        String(length=255), index=False, server_default="Available right Now"
    )

    get_started_button_text: Mapped[str | None] = mapped_column(
        String(length=255), index=False, server_default="Get it Now"
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
