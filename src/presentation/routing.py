"""Auth routing."""

from litestar import Router

from src.presentation.controllers.api.api_auth import AuthController
from src.presentation.controllers.api.api_health import HealthController
from src.presentation.controllers.cli.core import core_controller

auth_router = Router(
    path="/auth",
    route_handlers=[AuthController],
)


health_router = Router(
    path="/health",
    route_handlers=[HealthController],
    include_in_schema=False,
)


cli_router = [
    core_controller,
]
