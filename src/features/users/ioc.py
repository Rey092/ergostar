"""User provider (DI)."""

from dishka import Scope
from dishka import provide
from dishka.provider import Provider

from src.features.users.gateways import UserGateway


class UserProvider(Provider):
    """Subscription provider (DI)."""

    get_user_gateway = provide(
        source=UserGateway,
        scope=Scope.REQUEST,
    )
