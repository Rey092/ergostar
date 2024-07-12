"""Health router module."""
from litestar import Router

from src.core.presentation.api.health import HealthController

health_router = Router(
    path="/health",
    tags=["health"],
    route_handlers=[
        HealthController
    ]
)
