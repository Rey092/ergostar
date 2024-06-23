"""Subscription models."""

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SubscriptionPlan(BigIntAuditBase):
    """Subscription plan model."""

    __tablename__ = "subscriptions__plans"

    title: Mapped[str] = mapped_column(String(length=255), index=False)

    subtitle: Mapped[str] = mapped_column(String(length=255), index=False)

    monthly_price: Mapped[int] = mapped_column(Integer, index=False, nullable=True)

    annual_price: Mapped[int] = mapped_column(Integer, index=False, nullable=True)

    monthly_requests_limit: Mapped[int] = mapped_column(
        Integer, index=False, nullable=True
    )

    rate_limit: Mapped[int] = mapped_column(Integer, index=False, nullable=True)

    rate_period: Mapped[str] = mapped_column(
        String(length=255), index=False, nullable=True
    )

    is_available: Mapped[bool] = mapped_column(Boolean, index=False, default=False)

    __table_args__ = (
        # rate_limit and rate_period should be set together or not set at all
        CheckConstraint(
            "rate_limit IS NOT NULL AND rate_period IS NOT NULL "
            "OR rate_limit IS NULL AND rate_period IS NULL",
            name="rate_limit_rate_period_check",
        ),
        # monthly_price and annual_price should be set together or not set at all
        CheckConstraint(
            "monthly_price IS NOT NULL AND annual_price IS NOT NULL "
            "OR monthly_price IS NULL AND annual_price IS NULL",
            name="monthly_price_annual_price_check",
        ),
    )

    @property
    def rate_period_readable(self) -> str:
        """Return the rate period in human-readable format.

        It has format: 1m, 15m, 1h.

        Only minutes and hours are supported.

        If period is 1 minute or 1 hour, it should be returned in singular form.
        """
        number: int = int(self.rate_period[:-1])
        period: str = self.rate_period[-1]

        if period == "m":
            return "Minute" if number == 1 else f"{number} minutes"

        if period == "h":
            return "Hour" if number == 1 else f"{number} hours"

        return "Unknown"


# class Subscription(BigIntAuditBase):
#     """Subscription model."""
#
#     __tablename__ = "subscriptions__subscriptions"
#
#     user_id: Mapped[int] = mapped_column(
#         Integer,
#         index=False
#     )
#
#     plan_id: Mapped[int] = mapped_column(
#         Integer,
#         index=False
#     )
#
#     is_active: Mapped[bool] = mapped_column(
#         Boolean,
#         index=False,
#         default=True
#     )
#
#     __table_args__ = (
#         CheckConstraint(
#             "user_id IS NOT NULL AND plan_id IS NOT NULL",
#             name="user_plan_check",
#         ),
#     )
