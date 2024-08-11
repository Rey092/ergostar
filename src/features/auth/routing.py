"""Auth routing."""

from litestar import Router

from src.features.auth.controllers.auth import AuthController

auth_router = Router(
    path="/auth",
    route_handlers=[AuthController],
)
