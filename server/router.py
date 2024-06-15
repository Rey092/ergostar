"""Application Modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.landing.controller import LandingController

if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler


route_handlers: list[ControllerRouterHandler] = [LandingController]
