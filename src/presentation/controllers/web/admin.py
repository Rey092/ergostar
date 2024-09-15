"""Admin Controller."""

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller
from litestar import get
from litestar.response import Template

from src.application.interactors.admin.get_dashboard import GetDashboardInteractor


class AdminController(Controller):
    """Auth Controller."""

    @get("/")
    @inject
    async def create_api_key(
        self,
        interactor: FromDishka[GetDashboardInteractor],
    ) -> Template:
        """Create an api key.

        Excluded from auth.

        Rate limit: One request per 2 seconds.
        Rate limit is used to prevent spam and race conditions.
        """
        result = await interactor(request_model=None)
        return Template(template_name="admin/dashboard.html", context=result)
