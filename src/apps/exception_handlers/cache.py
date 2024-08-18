"""Cache exception handler for Litestar."""

from typing import Any

from cashews.exceptions import BackendNotAvailableError
from cashews.exceptions import CacheBackendInteractionError
from cashews.exceptions import CacheError
from cashews.exceptions import CircuitBreakerOpen
from cashews.exceptions import LockedError
from cashews.exceptions import NotConfiguredError
from cashews.exceptions import RateLimitError
from cashews.exceptions import SignIsMissingError
from cashews.exceptions import TagNotRegisteredError
from cashews.exceptions import UnSecureDataError
from cashews.exceptions import UnsupportedPicklerError
from cashews.exceptions import WrongKeyError
from litestar import Request
from litestar import Response
from litestar.exceptions import ClientException
from litestar.exceptions import HTTPException
from litestar.exceptions import InternalServerException
from litestar.exceptions import ServiceUnavailableException
from litestar.exceptions import TooManyRequestsException
from litestar.exceptions.responses import ExceptionResponseContent
from litestar.exceptions.responses import create_debug_response
from litestar.exceptions.responses import create_exception_response

from src.apps.exception_handlers import _HTTPConflictException


def cache_exception_handler(
    request: Request[Any, Any, Any],
    exc: CacheError,
) -> Response[ExceptionResponseContent]:
    """Transform cache-related exceptions to HTTP exceptions.

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
        case BackendNotAvailableError():
            http_exc = ServiceUnavailableException
        case NotConfiguredError() | UnsupportedPicklerError() | WrongKeyError():
            http_exc = ClientException
        case (
            UnSecureDataError()
            | SignIsMissingError()
            | TagNotRegisteredError()
            | CacheBackendInteractionError()
        ):
            http_exc = InternalServerException
        case LockedError():
            http_exc = _HTTPConflictException
        case RateLimitError():
            http_exc = TooManyRequestsException
        case CircuitBreakerOpen():
            http_exc = ServiceUnavailableException
        case _:
            http_exc = InternalServerException

    if request.app.debug:
        return create_debug_response(request, exc)

    return create_exception_response(
        request,
        http_exc(detail=str(exc)),
    )
