"""Litestar session middleware for storing session data."""

from __future__ import annotations

from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any
from typing import Generic

from litestar.connection import ASGIConnection
from litestar.middleware import AbstractMiddleware
from litestar.middleware._internal.exceptions import ExceptionHandlerMiddleware
from litestar.middleware.session.base import BaseSessionBackendT
from litestar.security.session_auth import SessionAuth
from litestar.types import ASGIApp
from litestar.types import Message
from litestar.types import Receive
from litestar.types import Scope
from litestar.types import Send


class ApiKeyMiddlewareWrapper:
    """Wrapper class that serves as the middleware entry point."""

    def __init__(self, app: ASGIApp, config: SessionAuth[Any, Any]) -> None:
        """Wrap the SessionAuthMiddleware inside ExceptionHandlerMiddleware, and it wraps this inside SessionMiddleware.
        This allows the auth middleware to raise exceptions and still have the response handled, while having the
        session cleared.

        Args:
            app: An ASGIApp, this value is the next ASGI handler to call in the middleware stack.
            config: An instance of SessionAuth.
        """
        self.app = app
        self.config = config
        self.has_wrapped_middleware = False

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Handle creating a middleware stack and calling it.

        Args:
            scope: The ASGI connection scope.
            receive: The ASGI receive function.
            send: The ASGI send function.

        Returns:
            None
        """
        if not self.has_wrapped_middleware:
            auth_middleware = self.config.authentication_middleware_class(
                app=self.app,
                exclude=self.config.exclude,
                exclude_http_methods=self.config.exclude_http_methods,
                exclude_opt_key=self.config.exclude_opt_key,
                scopes=self.config.scopes,
                retrieve_user_handler=self.config.retrieve_user_handler,  # type: ignore[arg-type]
            )
            exception_middleware = ExceptionHandlerMiddleware(
                app=auth_middleware, debug=None
            )
            self.app = self.config.session_backend_config.middleware.middleware(
                app=exception_middleware,
                backend=self.config.session_backend,
            )
            self.has_wrapped_middleware = True
        await self.app(scope, receive, send)


class ApiKeyMiddleware(AbstractMiddleware, Generic[BaseSessionBackendT]):
    """Litestar session middleware for storing session data."""

    def __init__(self, app: ASGIApp, backend: BaseSessionBackendT) -> None:
        """Initialize ``SessionMiddleware``

        Args:
            app: An ASGI application
            backend: A :class:`BaseSessionBackend` instance used to store and retrieve session data
        """
        super().__init__(
            app=app,
            exclude=backend.config.exclude,
            exclude_opt_key=backend.config.exclude_opt_key,
            scopes=backend.config.scopes,
        )
        self.backend = backend

    def create_send_wrapper(
        self, connection: ASGIConnection
    ) -> Callable[[Message], Awaitable[None]]:
        """Create a wrapper for the ASGI send function, which handles setting the cookies on the outgoing response.

        Args:
            connection: ASGIConnection

        Returns:
            None
        """

        async def wrapped_send(message: Message) -> None:
            """Wrap the ``send`` function.

            Declared in local scope to make use of closure values.

            Args:
                message: An ASGI message.

            Returns:
                None
            """
            if message["type"] != "http.response.start":
                await connection.send(message)
                return

            scope_session = connection.scope.get("session")

            await self.backend.store_in_message(scope_session, message, connection)
            await connection.send(message)

        return wrapped_send

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI-callable.

        Args:
            scope: The ASGI connection scope.
            receive: The ASGI receive function.
            send: The ASGI send function.

        Returns:
            None
        """
        connection = ASGIConnection[Any, Any, Any, Any](
            scope, receive=receive, send=send
        )
        scope["session"] = await self.backend.load_from_connection(connection)
        connection._connection_state.session_id = self.backend.get_session_id(
            connection
        )  # pyright: ignore [reportGeneralTypeIssues]

        await self.app(scope, receive, self.create_send_wrapper(connection))
