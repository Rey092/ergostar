"""Application Modules."""

from litestar.types import ControllerRouterHandler

from src.landing.presentations.main import LandingController
from src.landing.presentations.favicon import FaviconController
from src.landing.presentations.seo import SeoController


landing_router: list[ControllerRouterHandler] = [
    LandingController,
    FaviconController,
    SeoController
]
