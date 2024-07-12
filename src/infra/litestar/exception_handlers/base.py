from typing import Any

from litestar.connection import Request
from litestar.middleware.exceptions.middleware import ExceptionResponseContent
from litestar.response import Response
from advanced_alchemy.exceptions import IntegrityError
from litestar.exceptions import (
    HTTPException,
    InternalServerException,
    NotFoundException,
    PermissionDeniedException
)
from litestar.exceptions.responses import (
    create_debug_response,
    create_exception_response,
)
from litestar.repository.exceptions import ConflictError, NotFoundError, RepositoryError
from litestar.status_codes import HTTP_409_CONFLICT


class _HTTPConflictException(HTTPException):
    """Request conflict with the current state of the target resource."""

    status_code = HTTP_409_CONFLICT


def exception_to_http_response(
    request: Request[Any, Any, Any],
    exc: RepositoryError,
) -> Response[ExceptionResponseContent]:
    """Transform repository exceptions to HTTP exceptions.

    Args:
        request: The request that experienced the exception.
        exc: Exception raised during handling of the request.

    Returns:
        Exception response appropriate to the type of original exception.
    """
    http_exc: type[HTTPException]
    if isinstance(exc, NotFoundError):
        http_exc = NotFoundException
    elif isinstance(exc, ConflictError | RepositoryError | IntegrityError):
        http_exc = _HTTPConflictException
    # elif isinstance(exc, AuthorizationError):
    #     http_exc = PermissionDeniedException
    else:
        http_exc = InternalServerException
    if request.app.debug and http_exc not in (
        PermissionDeniedException,
        NotFoundError,
        # AuthorizationError
    ):
        return create_debug_response(request, exc)
    return create_exception_response(request, http_exc(detail=str(exc.__cause__)))
