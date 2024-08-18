"""Base exception handler for vault repository exceptions."""

from typing import Any

from hvac.exceptions import BadGateway
from hvac.exceptions import Forbidden
from hvac.exceptions import InternalServerError
from hvac.exceptions import InvalidPath
from hvac.exceptions import InvalidRequest
from hvac.exceptions import ParamValidationError
from hvac.exceptions import PreconditionFailed
from hvac.exceptions import RateLimitExceeded
from hvac.exceptions import Unauthorized
from hvac.exceptions import UnexpectedError
from hvac.exceptions import UnsupportedOperation
from hvac.exceptions import VaultDown
from hvac.exceptions import VaultError
from hvac.exceptions import VaultNotInitialized
from litestar.connection import Request
from litestar.exceptions import ClientException
from litestar.exceptions import HTTPException
from litestar.exceptions import InternalServerException
from litestar.exceptions import NotAuthorizedException
from litestar.exceptions import NotFoundException
from litestar.exceptions import PermissionDeniedException
from litestar.exceptions import ServiceUnavailableException
from litestar.exceptions import TooManyRequestsException
from litestar.exceptions.responses import create_debug_response
from litestar.exceptions.responses import create_exception_response
from litestar.middleware.exceptions.middleware import ExceptionResponseContent
from litestar.response import Response

from src.apps.exception_handlers import _HTTPBadGatewayException
from src.apps.exception_handlers import _HTTPConflictException


def repository_vault_exception_handler(
    request: Request[Any, Any, Any],
    exc: VaultError,
) -> Response[ExceptionResponseContent]:
    """Transform vault repository exceptions to HTTP exceptions.

    Args:
    ----
        request: The request that experienced the exception.
        exc: Exception raised during handling of the request.

    Returns:
    -------
        Exception response is appropriate to the type of original exception.

    """
    http_exc: type[HTTPException]

    match exc:
        case InvalidRequest() | ParamValidationError():
            http_exc = ClientException
        case Unauthorized():
            http_exc = NotAuthorizedException
        case Forbidden():
            http_exc = PermissionDeniedException
        case InvalidPath():
            http_exc = NotFoundException
        case PreconditionFailed():
            http_exc = _HTTPConflictException
        case RateLimitExceeded():
            http_exc = TooManyRequestsException
        case VaultError() | InternalServerError() | UnexpectedError():
            http_exc = InternalServerException
        case BadGateway():
            http_exc = _HTTPBadGatewayException
        case VaultDown() | VaultNotInitialized() | UnsupportedOperation():
            http_exc = ServiceUnavailableException
        case _:
            http_exc = InternalServerException

    if request.app.debug:
        return create_debug_response(request, exc)

    return create_exception_response(
        request,
        http_exc(detail=str(exc.__cause__)),
    )
