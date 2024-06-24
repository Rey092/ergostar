"""Core Controller Module."""

from pathlib import Path

from litestar import Controller
from litestar import MediaType
from litestar import get
from litestar.datastructures import CacheControlHeader
from litestar.response import File

from config import settings


class CoreController(Controller):
    """Core Controller."""

    include_in_schema = False
    opt = {"exclude_from_auth": True}

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

    @get(path="/health", media_type=MediaType.TEXT)
    async def health_check(self) -> str:
        """Health check."""
        return "ok"
