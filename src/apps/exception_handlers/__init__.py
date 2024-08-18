"""Missing litestar exceptions."""

from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_409_CONFLICT
from litestar.status_codes import HTTP_502_BAD_GATEWAY


class _HTTPConflictException(HTTPException):
    """Request conflict with the current state of the target resource."""

    status_code = HTTP_409_CONFLICT


class _HTTPBadGatewayException(HTTPException):
    """The Server received an invalid response from an upstream server."""

    status_code = HTTP_502_BAD_GATEWAY
