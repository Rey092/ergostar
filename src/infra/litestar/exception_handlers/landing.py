from litestar import Request
from litestar.exceptions import NotFoundException, InternalServerException
from litestar.response import Template


def not_found_exception_handler(_: Request, exc: NotFoundException) -> Template:
    """Handle 404 Not Found."""
    return Template(template_name="landing/exceptions/404.html", status_code=404)


def internal_server_exception_handler(
    _: Request, exc: InternalServerException
) -> Template:
    """Handle 500 Internal Server Error."""
    return Template(template_name="landing/exceptions/500.html", status_code=500)
