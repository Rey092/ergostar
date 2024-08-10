"""User provider (DI)."""

from dishka import Scope
from dishka import provide
from dishka.provider import Provider

from src.features.users.repositories.user import UserRepository


class UserProvider(Provider):
    """Subscription provider (DI)."""

    user_repository = provide(
        source=UserRepository,
        scope=Scope.REQUEST,
    )
