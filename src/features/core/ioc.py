"""Core provider module."""
from dishka import Scope, provide, Provider

from src.features.core.interactors.drop_database import DropDatabaseInteractor
from src.features.core.services.fixture_loader import FixtureLoaderService


class CoreProvider(Provider):
    """Core provider (DI)."""

    drop_database = provide(
        source=DropDatabaseInteractor,
        scope=Scope.REQUEST,
    )

    fixture_loader_service = provide(
        source=FixtureLoaderService,
        scope=Scope.REQUEST,
    )
