"""Core Controller Module."""

from litestar import Controller
from litestar import MediaType
from litestar import get


class HealthController(Controller):
    """Core Controller."""

    include_in_schema = False
    opt = {"exclude_from_auth": True}

    @get(path="/health", media_type=MediaType.JSON)
    async def health_check(self) -> dict:
        """Health check."""
        return {
            "status": "ok",
        }
