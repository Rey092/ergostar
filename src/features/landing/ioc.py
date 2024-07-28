"""Landing provider (DI)."""

from dishka import Scope, AnyOf
from dishka import provide
from dishka.provider import Provider
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.landing.interactors.get_faq import GetFaqInteractor
from src.features.landing.interactors.get_home import GetHomeInteractor
from src.features.landing.interactors.get_pricing import GetPricingInteractor
from src.features.landing.interactors.interfaces import IGetOneLandingSettings, \
    IGetOneLandingHomePage, IGetCarouserLandingSolutions, IListActiveLandingSnippets, IListPublicSubscriptionPlans
from src.features.landing.interactors.seed.interfaces import ISeedLandingSettings
from src.features.landing.interactors.seed.landing_settings import SeedLandingSettingsInteractor
from src.features.landing.repositories import (
    LandingHomePageRepository,
    LandingSolutionRepository,
    LandingSnippetRepository,
    LandingSettingsRepository
)
from src.features.landing.repositories.subscription_plan import LandingSubscriptionPlansRepository


class LandingProvider(Provider):
    """Landing provider (DI)."""

    landing_settings_repository = provide(
        source=LandingSettingsRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            IGetOneLandingSettings,
            ISeedLandingSettings,
        ]
    )

    landing_home_page_repository = provide(
        source=LandingHomePageRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            IGetOneLandingHomePage
        ]
    )

    landing_solution_repository = provide(
        source=LandingSolutionRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            IGetCarouserLandingSolutions
        ]
    )

    landing_snippet_repository = provide(
        source=LandingSnippetRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            IListActiveLandingSnippets
        ]
    )

    landing_subscription_plans_repository = provide(
        source=LandingSubscriptionPlansRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            IListPublicSubscriptionPlans
        ]
    )

    get_home_interactor = provide(
        source=GetHomeInteractor,
        scope=Scope.REQUEST
    )

    get_faq_interactor = provide(
        source=GetFaqInteractor,
        scope=Scope.REQUEST
    )

    get_pricing_interactor = provide(
        source=GetPricingInteractor,
        scope=Scope.REQUEST
    )

    seed_landing_settings_interactor = provide(
        source=SeedLandingSettingsInteractor,
        scope=Scope.REQUEST
    )
