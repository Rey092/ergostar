"""Server exception handler."""

import logging
from typing import Any

from litestar import Request
from litestar import Response
from litestar.exceptions.responses import ExceptionResponseContent
from litestar.exceptions.responses import create_debug_response
from litestar.exceptions.responses import create_exception_response


def server_exception_handler(
    request: Request[Any, Any, Any],
    exc: Exception,
) -> Response[ExceptionResponseContent]:
    """Uncaught exception handler."""
    logging.error("Server error", exc_info=exc)
    if request.app.debug:
        return create_debug_response(request, exc)
    return create_exception_response(
        request,
        exc,
    )
