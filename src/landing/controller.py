from litestar import Controller, get
from litestar.response import Template
from litestar.status_codes import HTTP_200_OK
from config import constants


class LandingController(Controller):
    """Landing Controller."""

    include_in_schema = False
    opt = {"exclude_from_auth": True}

    @get(
        path=[constants.SITE_INDEX, f"{constants.SITE_INDEX}/{{path:str}}"],
        name="landing:home",
        status_code=HTTP_200_OK,
    )
    async def home(self, path: str | None = None) -> Template:
        """Serve site root."""
        return Template(template_name="landing/pages/home.html", context={"path": path})

    @get(
        path="/faq",
        name="landing:faq",
    )
    async def faq(self, path: str | None = None) -> Template:
        """Serve site root."""
        return Template(template_name="landing/pages/faq.html", context={"path": path})

    @get(
        path="/pricing",
        name="landing:pricing",
    )
    async def pricing(self, path: str | None = None) -> Template:
        """Serve site root."""
        return Template(
            template_name="landing/pages/pricing.html", context={"path": path}
        )
