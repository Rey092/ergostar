"""Landing routing module."""
from litestar import Router

from src.features.landing.controllers.favicon import FaviconController
from src.features.landing.controllers.main import LandingController
from src.features.landing.controllers.seo import SeoController

landing_router = Router(
    path="/",
    route_handlers=[
        LandingController,
        FaviconController,
        SeoController
    ],
    include_in_schema=False,
    opt={"exclude_from_auth": True}
)
