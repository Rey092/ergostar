"""Auth API Key Configuration."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import cast

from litestar.middleware.base import DefineMiddleware
from litestar.openapi.spec import Components
from litestar.openapi.spec import SecurityRequirement
from litestar.openapi.spec import SecurityScheme
from litestar.security.base import AbstractSecurityConfig

from src.features.auth.security.api_key.middleware import ApiKeyMiddleware
from src.features.users.entities.userentity import UserEntity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from collections.abc import Sequence

    from litestar.connection import ASGIConnection
    from litestar.di import Provide
    from litestar.types import ControllerRouterHandler
    from litestar.types import Guard
    from litestar.types import Method
    from litestar.types import Scopes
    from litestar.types import SyncOrAsyncUnion
    from litestar.types import TypeEncodersMap

UserType = TypeVar("UserType", bound=UserEntity)

__all__ = ("ApiKeyAuth",)


@dataclass
class ApiKeyAuth(Generic[UserType], AbstractSecurityConfig[UserType, str]):
    """Session-Based Security Backend."""

    retrieve_user_handler: Callable[[Any, ASGIConnection], SyncOrAsyncUnion[Any | None]]
    """Callable that receives the ``auth`` value from the
    authentication middleware and returns a ``user`` value."""

    authentication_middleware_class: type[ApiKeyMiddleware] = field(
        default=ApiKeyMiddleware,
    )
    """
    The authentication middleware class to use.
    """

    guards: Iterable[Guard] | None = field(default=None)
    """An iterable of guards to call for requests, providing
    authorization functionalities."""

    exclude: str | list[str] | None = field(default=None)
    """A pattern or list of patterns to skip in the authentication middleware."""

    exclude_opt_key: str = field(default="exclude_from_auth")
    """An identifier to use on routes to disable authentication
    and authorization checks for a particular route."""

    exclude_http_methods: Sequence[Method] | None = field(
        default_factory=lambda: cast("Sequence[Method]", ["OPTIONS", "HEAD"]),
    )
    """A sequence of http methods that do not require authentication.
    Defaults to ['OPTIONS', 'HEAD']"""

    scopes: Scopes | None = field(default=None)
    """ASGI scopes processed by the authentication middleware, if ``None``,
    both ``http`` and ``websocket`` will be processed."""

    route_handlers: Iterable[ControllerRouterHandler] | None = field(default=None)
    """An optional iterable of route handlers to register."""

    dependencies: dict[str, Provide] | None = field(default=None)
    """An optional dictionary of dependency providers."""

    type_encoders: TypeEncodersMap | None = field(default=None)
    """A mapping of types to callables that transform them into types
    supported for serialization."""

    auth_header: str = field(default="X-Api-Key")
    """
    Request header key from which to retrieve the token.
    """

    openapi_security_scheme_name: str = field(default="ApiKeyAuth")
    """The value to use for the OpenAPI security scheme and security requirements."""

    description: str = field(default="JWT api-key authentication and authorization.")
    """Description for the OpenAPI security scheme."""

    @property
    def middleware(self) -> DefineMiddleware:
        """Insert the config into a middleware list on one of the application layers."""
        return DefineMiddleware(
            self.authentication_middleware_class,
            auth_header=self.auth_header,
            exclude=self.exclude,
            exclude_opt_key=self.exclude_opt_key,
            exclude_http_methods=self.exclude_http_methods,
            retrieve_user_handler=self.retrieve_user_handler,
            scopes=self.scopes,
        )

    @property
    def openapi_components(self) -> Components:
        """Create OpenAPI documentation for the Session Authentication schema used.

        Returns:
            An :class: `OpenAPI Component instance.
        """
        return Components(
            security_schemes={
                self.openapi_security_scheme_name: SecurityScheme(
                    type="apiKey",
                    name=self.auth_header,
                    security_scheme_in="header",
                    description="Header API key authentication.",
                ),
            },
        )

    @property
    def security_requirement(self) -> SecurityRequirement:
        """Return OpenAPI 3.1.

        Returns:
            OpenAPI 3.1: SecurityRequirement dictionary.
        """
        return {self.openapi_security_scheme_name: []}
