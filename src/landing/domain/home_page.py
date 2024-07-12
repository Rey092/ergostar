"""Landing home page entity."""
from dataclasses import field, dataclass
from datetime import datetime, timezone


@dataclass
class LandingHomePage:
    """Home page model."""

    id: int = field(init=False, default=None)
    subtitle_1: str = "Powerful & Versatile"
    subtitle_2: str = "API Services for Modern Applications"
    description: str = ("Enhance your applications with Ergolon API's wide range of services, "
                        "from email and phone validation to advanced AI functionalities. "
                        "Seamlessly integrate our APIs to boost your app's performance and capabilities.")
    you_get_label: str = "Futures"
    you_get_title: str = "What you will get with Ergostar API"
    you_get_subtitle: str | None = ("Our API services are designed to help you build"
                                    " powerful and versatile applications.")
    you_get_block_1_title: str = "Dashboard"
    you_get_block_1_description: str = ("Get a bird's eye view of your account and manage your "
                                        "API keys, usage, and billing information.")
    you_get_block_1_feather_icon: str = "pie-chart"
    you_get_block_2_title: str = "Save money"
    you_get_block_2_description: str = "Save money by using our versatile range of API services."
    you_get_block_2_feather_icon: str = "dollar-sign"
    you_get_block_3_title: str = "Boost Performance"
    you_get_block_3_description: str = "Boost your app's performance and capabilities by integrating our APIs."
    you_get_block_3_feather_icon: str = "trending-up"
    you_get_block_4_title: str = "Documentation"
    you_get_block_4_description: str = "Access our comprehensive documentation to learn more about our API services."
    you_get_block_4_feather_icon: str = "book"
    get_started_label: str = "Get Started"
    get_started_title: str = "Ergolon saves"
    get_started_array: str = '"Time", "Money", "Effort"'
    get_started_description: str | None = ("Ergolon API saves you tons of hard work and time by "
                                           "providing you with a wide range of services to enhance "
                                           "your applications.")
    get_started_lower_title: str | None = "Available right Now"
    get_started_button_text: str | None = "Get it Now"

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
