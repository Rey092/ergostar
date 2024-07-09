"""Application Modules."""

from litestar.types import ControllerRouterHandler

from src.presentation.landing.main import LandingController
from src.presentation.landing.favicon import FaviconController
from src.presentation.landing.seo import SeoController


landing_router: list[ControllerRouterHandler] = [
    LandingController,
    FaviconController,
    SeoController
]
