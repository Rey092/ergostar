"""Favicon Controller."""

from pathlib import Path
from litestar import Controller
from litestar import get
from litestar.datastructures import CacheControlHeader
from litestar.response import File

from src.config import settings


class FaviconController(Controller):
    """Favicon Controller."""

    @get(
        path="/favicon.ico",
        name="core:favicon",
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    async def get_favicon(self) -> File:
        """Serve favicon."""
        return File(
            path=Path(settings.app.BASE_DIR, "static", "favicon", "favicon.ico"),
            filename="favicon.ico",
        )
