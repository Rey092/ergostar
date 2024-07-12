"""Landing models."""
from datetime import timezone, datetime

from advanced_alchemy.base import orm_registry
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Boolean, Table, DateTime, BigInteger
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text

from src.domain.entities.landing.home_page import LandingHomePage
from src.domain.entities.landing.settings import LandingSettings
from src.domain.entities.landing.snippet import LandingSnippet
from src.domain.entities.landing.solution import LandingSolution

landing_settings_table = Table(
    "landing__settings",
    orm_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("title", String(length=255), index=False, default="Ergostar", nullable=False),
    Column(
        "footer_description",
        Text,
        index=False,
        default="Ergostar API provides a wide range of services to "
                "enhance your applications. From email and phone "
                "validation to VAT number validation, IP geolocation,"
                " WHOIS data, and advanced AI functionalities.",
    ),
    Column(
        "footer_rights",
        Text,
        index=False,
        default="© 2024 Ergostar. All rights reserved.",
        nullable=False,
    ),
    Column(
        "url_login",
        String(length=255),
        index=False,
        nullable=False,
        default="/login/",
    ),
    Column(
        "url_api_docs",
        String(length=255),
        index=False,
        nullable=False,
        default="/api/docs/"
    ),
    Column(
        "url_register",
        String(length=255),
        index=False,
        nullable=False,
        default="/register/",
    ),
    Column(
        "created_at", DateTime,
        index=False,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    ),
    Column(
        "updated_at", DateTime,
        index=False,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    ),
)

landing_home_page_table = Table(
    "landing__home_page",
    orm_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column(
        "subtitle_1",
        String(length=255),
        index=False,
        nullable=False,
        default="Powerful & Versatile"
    ),
    Column(
        "subtitle_2",
        String(length=255),
        index=False,
        nullable=False,
        default="API Services for Modern Applications",
    ),
    Column(
        "description",
        Text,
        index=False,
        nullable=False,
        default="Enhance your applications with Ergolon API's wide range of services, "
                "from email and phone validation to advanced AI functionalities. Seamlessly "
                "integrate our APIs to boost your app's performance and capabilities.",
    ),
    Column(
        "you_get_label",
        String(length=255),
        index=False,
        nullable=False,
        default="Futures",
    ),
    Column(
        "you_get_title",
        String(length=255),
        index=False,
        nullable=False,
        default="What you will get with Ergostar API",
    ),
    Column(
        "you_get_subtitle",
        String(length=255),
        index=False,
        nullable=False,
        default="Our API services are designed to help "
                "you build powerful and versatile applications.",
    ),
    Column(
        "you_get_block_1_title",
        String(length=255),
        index=False,
        nullable=False,
        default="Dashboard",
    ),
    Column(
        "you_get_block_1_description",
        Text,
        index=False,
        nullable=False,
        default="Get a bird's eye view of your "
                "account and manage your API keys, "
                "usage, and billing information.",
    ),
    Column(
        "you_get_block_1_feather_icon",
        String(length=40),
        index=False,
        nullable=False,
        default="pie-chart",
    ),
    Column(
        "you_get_block_2_title",
        String(length=255),
        index=False,
        nullable=False,
        default="Save money",
    ),
    Column(
        "you_get_block_2_description",
        Text,
        index=False,
        nullable=False,
        default="Save money by using our versatile range of API services.",
    ),
    Column(
        "you_get_block_2_feather_icon",
        String(length=40),
        index=False,
        nullable=False,
        default="dollar-sign",
    ),
    Column(
        "you_get_block_3_title",
        String(length=255),
        index=False,
        nullable=False,
        default="Boost Performance",
    ),
    Column(
        "you_get_block_3_description",
        Text,
        index=False,
        nullable=False,
        default="Boost your app's performance "
                "and capabilities by integrating our APIs.",
    ),
    Column(
        "you_get_block_3_feather_icon",
        String(length=40),
        index=False,
        nullable=False,
        default="trending-up",
    ),
    Column(
        "you_get_block_4_title",
        String(length=255),
        index=False,
        nullable=False,
        default="Documentation",
    ),
    Column(
        "you_get_block_4_description",
        Text,
        index=False,
        nullable=False,
        default="Access our comprehensive documentation to "
                "learn more about our API services.",
    ),
    Column(
        "you_get_block_4_feather_icon",
        String(length=40),
        index=False,
        nullable=False,
        default="book",
    ),
    Column(
        "get_started_label",
        String(length=255),
        index=False,
        nullable=False,
        default="Get Started",
    ),
    Column(
        "get_started_title",
        String(length=255),
        index=False,
        nullable=False,
        default="Ergolon saves",
    ),
    Column(
        "get_started_array",
        String(length=255),
        index=False,
        nullable=False,
        default='"Time", "Money", "Effort"',
    ),
    Column(
        "get_started_description",
        Text,
        index=False,
        nullable=False,
        default="Ergolon API saves you tons of hard work and time by providing "
                "you with a wide range of services to enhance your applications.",
    ),
    Column(
        "get_started_lower_title",
        String(length=255),
        index=False,
        nullable=False,
        default="Available right Now",
    ),
    Column(
        "get_started_button_text",
        String(length=255),
        index=False,
        nullable=False,
        default="Get it Now",
    ),
    Column(
        "created_at",
        DateTime,
        index=False,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    ),
    Column(
        "updated_at",
        DateTime,
        index=False,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    ),
)

landing_solution_table = Table(
    "landing__solution",
    orm_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("title", String(length=255), index=False, nullable=False),
    Column("title_carousel", String(length=255), index=False, nullable=False),
    Column("description", Text, index=False, nullable=False),
    Column("is_top_active", Boolean, index=True, nullable=False, default=True),
    Column("is_carousel_active", Boolean, index=True, nullable=False, default=True),
    Column("docs_url", String(length=255), index=False, nullable=False, default="https://google.com"),
    Column("file", FileType(storage=FileSystemStorage(path="./media"), length=255), nullable=True),
    Column("created_at", DateTime, index=False, nullable=False, default=lambda: datetime.now(timezone.utc)),
    Column(
        "updated_at", DateTime, index=False, nullable=False,
        default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    ),
)


landing_snippet_table = Table(
    "landing__snippet",
    orm_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("tab", String(length=255), nullable=False, index=False),
    Column("title", String(length=255), nullable=False, index=False),
    Column("subtitle", String(length=255), nullable=False, index=False),
    Column("description", Text, nullable=False, index=False),
    Column("is_active", Boolean, index=True, nullable=False, default=True),
    Column("code", Text, nullable=False, index=False),
    Column("code_language", String(length=20), index=False, nullable=False),
    Column("feather_icon", String(length=40), index=False, nullable=False, default="test"),
    Column("created_at", DateTime, index=False, nullable=False, default=lambda: datetime.now(timezone.utc)),
    Column(
        "updated_at", DateTime, index=False, nullable=False,
        default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    ),
)

# map the models to the tables
orm_registry.map_imperatively(LandingSettings, landing_settings_table)
orm_registry.map_imperatively(LandingHomePage, landing_home_page_table)
orm_registry.map_imperatively(LandingSolution, landing_solution_table)
orm_registry.map_imperatively(LandingSnippet, landing_snippet_table)
