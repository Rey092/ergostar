from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Request, Response
from litestar.exceptions import NotFoundException, InternalServerException
from litestar.exceptions.responses import create_debug_response
from litestar.response import Template

from src.config.settings import AppSettings


def not_found_exception_handler(
    _: Request,
    exc: NotFoundException
) -> Template:
    """Handle 404 Not Found."""
    return Template(template_name="landing/exceptions/404.html", status_code=404)


class InternalServerExceptionHandler:
    """Internal Server Error handler"""

    def __init__(self, debug: bool):
        """Initialize handler."""
        self.debug = debug

    def __call__(self, _: Request, exc: InternalServerException) -> Response | Template:
        """Handle 500 Internal Server Error."""
        if self.debug:
            return create_debug_response(_, exc)
        return Template(template_name="landing/exceptions/500.html", status_code=500)
