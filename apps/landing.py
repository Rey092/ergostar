"""Prepare ASGI application for landing."""

from litestar import Litestar
from apps.builder import LitestarBuilder


class LandingLitestarBuilder(LitestarBuilder):
    """Litestar application builder."""

    pass


builder: LandingLitestarBuilder = LandingLitestarBuilder()
app: Litestar = builder.build()
