"""Health router module."""
from litestar import Router

from src.features.core.controllers.health import HealthController

health_router = Router(
    path="/health",
    route_handlers=[
        HealthController
    ],
    include_in_schema=False
)
