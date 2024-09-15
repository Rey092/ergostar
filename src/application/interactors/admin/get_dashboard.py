"""GetAdminHomePageInteractor."""

from src.application.common.interactor import Interactor


class GetDashboardInteractor(
    Interactor[None, None],
):
    """AuthenticateApiKeyInteractor."""

    def __init__(
        self,
    ):
        """Initialize interactor."""

    async def __call__(
        self,
        request_model: None = None,
    ) -> None:
        """Authenticate an API key."""
        return
