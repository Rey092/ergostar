"""Landing admin."""

from sqladmin import ModelView
from db.models import LandingSettings, LandingHomePage


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
