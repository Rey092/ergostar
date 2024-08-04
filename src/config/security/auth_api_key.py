"""Auth API Key Configuration."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Generic

from litestar.middleware.base import DefineMiddleware
from litestar.middleware.session.base import BaseSessionBackendT
from litestar.openapi.spec import Components
from litestar.openapi.spec import SecurityRequirement
from litestar.openapi.spec import SecurityScheme
from litestar.security.base import AbstractSecurityConfig
from litestar.security.base import UserType

__all__ = ("ApiKeyAuth",)


from src.config.security.middleware_api_key import ApiKeyMiddleware
from src.config.security.middleware_api_key import ApiKeyMiddlewareWrapper


@dataclass
class ApiKeyAuth(
    Generic[UserType, BaseSessionBackendT],
    AbstractSecurityConfig[UserType, dict[str, Any]],
):
    """Session-Based Security Backend."""

    # api_key_backend_config: BaseBackendConfig[BaseSessionBackendT]  # pyright: ignore
    # """A session backend config."""
    # retrieve_user_handler: Callable[[Any, ASGIConnection], SyncOrAsyncUnion[Any | None]]
    # """Callable that receives the ``auth`` value from the authentication middleware and returns a ``user`` value.

    authentication_middleware_class: type[ApiKeyMiddleware] = field(
        default=ApiKeyMiddleware
    )  # pyright: ignore
    """The authentication middleware class to use.

    Must inherit from :class:`SessionAuthMiddleware <litestar.security.session_auth.middleware.SessionAuthMiddleware>`
    """

    @property
    def middleware(self) -> DefineMiddleware:
        """Use this property to insert the config into a middleware list on one of the application layers."""
        return DefineMiddleware(ApiKeyMiddlewareWrapper, config=self)

    # @property
    # def session_backend(self) -> BaseSessionBackendT:
    #     """Create a session backend.
    #
    #     Returns:
    #         A subclass of: class:`BaseSessionBackend <litestar.middleware.session.base.BaseSessionBackend>`
    #     """
    #     return self.api_key_backend_config._backend_class(config=self.api_key_backend_config)  # pyright: ignore

    @property
    def openapi_components(self) -> Components:
        """Create OpenAPI documentation for the Session Authentication schema used.

        Returns:
            An :class: `Components <litestar.openapi.spec.components.Components>` instance.
        """
        return Components(
            security_schemes={
                "apiKey": SecurityScheme(
                    type="apiKey",
                    name="X-API-Key",
                    security_scheme_in="header",  # pyright: ignore
                    description="Header API key authentication.",
                ),
            },
        )

    @property
    def security_requirement(self) -> SecurityRequirement:
        """Return OpenAPI 3.1.

        :data:`SecurityRequirement <.openapi.spec.SecurityRequirement>` for the auth
        backend.

        Returns:
            An OpenAPI 3.1: data:`SecurityRequirement <.openapi.spec.SecurityRequirement>` dictionary.
        """
        return {"apiKey": []}
