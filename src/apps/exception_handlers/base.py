"""Base exception handler for repository exceptions."""

from typing import Any

from advanced_alchemy.exceptions import IntegrityError
from litestar.connection import Request
from litestar.exceptions import HTTPException
from litestar.exceptions import InternalServerException
from litestar.exceptions import NotFoundException
from litestar.exceptions import PermissionDeniedException
from litestar.exceptions.responses import create_debug_response
from litestar.exceptions.responses import create_exception_response
from litestar.middleware.exceptions.middleware import ExceptionResponseContent
from litestar.repository.exceptions import ConflictError
from litestar.repository.exceptions import NotFoundError
from litestar.repository.exceptions import RepositoryError
from litestar.response import Response
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
    ----
        request: The request that experienced the exception.
        exc: Exception raised during handling of the request.

    Returns:
    -------
        Exception response appropriates to the type of original exception.

    """
    http_exc: type[HTTPException]
    if isinstance(exc, NotFoundError):
        http_exc = NotFoundException
    elif isinstance(exc, ConflictError | RepositoryError | IntegrityError):
        http_exc = _HTTPConflictException
    else:
        http_exc = InternalServerException
    if request.app.debug and http_exc not in (
        PermissionDeniedException,
        NotFoundError,
    ):
        return create_debug_response(request, exc)
    return create_exception_response(
        request,
        http_exc(detail=str(exc.__cause__)),
    )
