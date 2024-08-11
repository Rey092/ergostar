"""Vault exception handler."""

from typing import Any

from hvac.exceptions import VaultError
from litestar import Request
from litestar import Response
from litestar.exceptions import ServiceUnavailableException
from litestar.exceptions.responses import create_debug_response
from litestar.exceptions.responses import create_exception_response

from src.features.users.entities.user import User


def vault_exception_handler(
    request: Request[User, str, Any],
    exc: VaultError,
) -> Response | Any:
    """Handle 404 Not Found."""
    if request.app.debug:
        return create_debug_response(request, exc)
    return create_exception_response(
        request,
        ServiceUnavailableException(detail=str(exc.__cause__)),
    )
