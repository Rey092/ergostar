"""Subscription models."""

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SubscriptionPlanModel(BigIntAuditBase):
    """Subscription Plan."""

    __tablename__ = "subscription_plans"

    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(length=255), nullable=False)
    monthly_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    annual_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    monthly_requests_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rate_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rate_period: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_public: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true",
        index=True,
    )
