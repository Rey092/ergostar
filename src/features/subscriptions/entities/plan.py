"""Subscription plan entity."""

from src.common.base.entity import Entity


class SubscriptionPlan(Entity):
    """Subscription plan model."""

    title: str
    subtitle: str
    monthly_price: int | None
    annual_price: int | None
    monthly_requests_limit: int | None
    rate_limit: int | None
    rate_period: str | None
    is_public: bool

    @property
    def rate_period_verbose(self) -> str:
        """Return the rate period in human-readable format.

        It has format: 1m, 15m, 1h.

        Only minutes and hours are supported.

        If the period is 1 minute or 1 hour, it should be returned in singular form.
        """
        number: int = int(self.rate_period[:-1]) if self.rate_period else 0
        period: str = self.rate_period[-1] if self.rate_period else ""

        if period == "m":
            return "Minute" if number == 1 else f"{number} minutes"

        if period == "h":
            return "Hour" if number == 1 else f"{number} hours"

        return "Unknown"
