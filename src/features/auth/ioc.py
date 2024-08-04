"""Auth provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.features.auth.gateways.api_key import ApiKeyGateway
from src.features.auth.use_cases.create_api_key import CreateApiKeyUseCase
from src.features.auth.use_cases.interfaces import ICreateApiKeyGateway


class AuthProvider(Provider):
    """Auth provider (DI)."""

    create_api_key_use_case = provide(
        source=CreateApiKeyUseCase,
        scope=Scope.REQUEST,
    )

    api_key_gateway = provide(
        source=ApiKeyGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[ICreateApiKeyGateway],
    )
