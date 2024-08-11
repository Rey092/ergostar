"""Litestar session middleware for storing session data."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Generic

from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware
from litestar.middleware import AuthenticationResult
from litestar.middleware.session.base import BaseSessionBackendT

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from collections.abc import Callable
    from collections.abc import Sequence

    from litestar.connection import ASGIConnection
    from litestar.types import ASGIApp
    from litestar.types import Method
    from litestar.types import Scopes

    from src.features.users.entities.user import User


class ApiKeyMiddleware(AbstractAuthenticationMiddleware, Generic[BaseSessionBackendT]):
    """Litestar session middleware for storing session data."""

    def __init__(
        self,
        app: ASGIApp,
        auth_header: str,
        exclude: str | list[str] | None,
        exclude_opt_key: str,
        exclude_http_methods: Sequence[Method] | None,
        retrieve_user_handler: Callable[
            [str, ASGIConnection[Any, Any, Any, Any]],
            Awaitable[Any],
        ],
        scopes: Scopes,
    ) -> None:
        """Check incoming requests for an api key in the auth header.

        If present, retrieve the user from persistence using the provided function.

        Args:
            app: An ASGIApp, this value is the next ASGI handler
            to call in the middleware stack.
            auth_header: Request header key from which to retrieve the token.
            E.g. ``Authorization`` or ``X-Api-Key``.
            exclude: A pattern or list of patterns to skip.
            exclude_opt_key: An identifier to use on routes to disable authentication
             for a particular route.
            exclude_http_methods: A sequence of http methods that do
            not require authentication.
            retrieve_user_handler: A function that receives a: class:
            `Token <.security.jwt.Token>`
            and returns a user, which can be any arbitrary value.
            scopes: ASGI scopes processed by the authentication middleware.
        """
        super().__init__(
            app=app,
            exclude=exclude,
            exclude_http_methods=exclude_http_methods,
            exclude_from_auth_key=exclude_opt_key,
            scopes=scopes,
        )
        self.auth_header = auth_header
        self.retrieve_user_handler = retrieve_user_handler
        self._exception_no_auth_header = "No API key found in request header"

    async def authenticate_request(
        self,
        connection: ASGIConnection[Any, Any, Any, Any],
    ) -> AuthenticationResult:
        """Given an HTTP Connection, parse the api key from header.

        Retrieve the user correlating to the api key from DB.

        Args:
            connection: An Litestar HTTPConnection instance.

        Raises:
            NotAuthorizedException: If token is invalid or user is not found.

        Returns:
            AuthenticationResult
        """
        api_key = connection.headers.get(self.auth_header)
        if not api_key:
            raise NotAuthorizedException(self._exception_no_auth_header)
        return await self.authenticate_api_key(api_key=api_key, connection=connection)

    async def authenticate_api_key(
        self,
        api_key: str,
        connection: ASGIConnection[Any, Any, Any, Any],
    ) -> AuthenticationResult:
        """Given an encoded JWT token, parse, validate and look up sub within token.

        Args:
            api_key: Encoded JWT token.
            connection: An ASGI connection instance.

        Raises:
            NotAuthorizedException: If token is invalid or user is not found.

        Returns:
            AuthenticationResult
        """
        user: User = await self.retrieve_user_handler(api_key, connection)
        return AuthenticationResult(user=user, auth=api_key)
