"""Dashboard app exception handlers."""

from litestar import Request
from litestar import Response
from litestar.exceptions import InternalServerException
from litestar.exceptions import NotFoundException
from litestar.exceptions.responses import create_debug_response
from litestar.response import Template

from src.main.config.settings import AppSettings


def not_found_exception_handler(
    _: Request,
    exc: NotFoundException,
) -> Template:
    """Handle 404 Not Found."""
    return Template(
        template_name="dashboard/exceptions/404.html",
        status_code=404,
    )


class InternalServerExceptionHandler:
    """Internal Server Error handler."""

    def __init__(self, app_settings: AppSettings):
        """Initialize handler."""
        self.debug = app_settings.DEBUG

    def __call__(
        self,
        _: Request,
        exc: InternalServerException,
    ) -> Response | Template:
        """Handle 500 Internal Server Error."""
        if self.debug:
            return create_debug_response(_, exc)
        return Template(
            template_name="dashboard/exceptions/500.html",
            status_code=500,
        )
