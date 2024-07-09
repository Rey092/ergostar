"""Landing admin."""

from sqladmin import ModelView
from sqlalchemy.orm import declarative_base

from src.domain.entities.landing import LandingSolution
from src.domain.entities.landing import LandingHomePage
from src.domain.entities.landing import LandingSettings


# base = declarative_base()
#
# class LandingSettings(LandingSettings, base):
#     pass


class LandingSettingsAdmin(ModelView, model=LandingSettings):  # type: ignore
    """Admin for landing settings."""

    column_list = [LandingSettings.id, LandingSettings.title]
    form_excluded_columns = [LandingSettings.created_at]

    can_create = False
    can_delete = False

    category = "Landing"
    icon = "fa-solid fa-gear"


class LandingHomePageAdmin(ModelView, model=LandingHomePage):  # type: ignore
    """Admin for landing home page."""

    column_list = [LandingHomePage.id, LandingHomePage.subtitle_1]
    form_excluded_columns = [LandingHomePage.created_at]

    can_create = False
    can_delete = False

    category = "Landing"
    icon = "fa-solid fa-home"


class LandingServiceAdmin(ModelView, model=LandingSolution):  # type: ignore
    """Admin for landing services."""

    column_list = [
        LandingSolution.id,
        LandingSolution.title,
        LandingSolution.is_top_active,
        LandingSolution.is_carousel_active,
    ]
    form_excluded_columns = [LandingSolution.created_at]

    category = "Landing"
    icon = "fa-solid fa-cogs"
