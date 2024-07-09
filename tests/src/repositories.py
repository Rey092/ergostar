"""Interfaces for Landing Home Page Repositories."""

from abc import abstractmethod
from collections.abc import Sequence

import factory
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from src.domain.entities.landing import LandingHomePage
from src.domain.entities.landing import LandingSettings
from src.domain.entities.landing import LandingSnippet
from src.domain.entities.landing import LandingSolution
from src.application.services.interfaces.repositories import (
    LandingHomePageRepositoryInterface,
)
from src.application.services.interfaces.repositories import (
    LandingSettingsRepositoryInterface,
)
from src.application.services.interfaces.repositories import (
    LandingSnippetRepositoryInterface,
)
from src.application.services.interfaces.repositories import (
    LandingSolutionRepositoryInterface,
)


class MockLandingHomePageRepository(LandingHomePageRepositoryInterface):
    """LandingHomePage Repository."""

    model_type = LandingHomePage


class MockLandingSettingsRepository(LandingSettingsRepositoryInterface):
    """LandingSettings Repository."""

    model_type = LandingSettings


# class LandingSnippetFactory(ModelFactory[LandingSnippet]):
#     """LandingSnippet Factory."""
#
#     model = LandingSnippet
engine = create_engine("sqlite://")
session = scoped_session(sessionmaker(bind=engine))


class LandingSnippetFactory(factory.alchemy.SQLAlchemyModelFactory):
    """LandingSnippet Factory."""

    class Meta:
        model = LandingSnippet
        sqlalchemy_session = session

    # username = 'john'
    tab = factory.Faker("word")
    title = factory.Faker("word")


class MockLandingSnippetRepository(LandingSnippetRepositoryInterface):
    """LandingSnippet Repository."""

    model_type = LandingSnippet

    async def list_active(self) -> Sequence[LandingSnippet]:
        """List active snippets."""
        return LandingSnippetFactory.create_batch(10)


class MockLandingSolutionRepository(LandingSolutionRepositoryInterface):
    """LandingSolution Repository."""

    model_type = LandingSolution

    @abstractmethod
    async def list_active_solutions_for_carousel(self) -> Sequence[LandingSolution]:
        """Get LandingSolutions for carousel string."""

    @abstractmethod
    async def list_top_banners(self) -> Sequence[LandingSolution]:
        """List top banners."""
