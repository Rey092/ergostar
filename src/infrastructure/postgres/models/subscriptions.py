"""Subscription models."""

from sqlalchemy import Column, BigInteger
from sqlalchemy import Integer
from sqlalchemy import String
from advanced_alchemy.base import orm_registry
from sqlalchemy import Boolean, Table

from src.domain.entities.subscriptions.plan import SubscriptionPlan

subscription_plan_table = Table(
    "subscriptions__plans",
    orm_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("title", String(length=255), nullable=False, index=False),
    Column("subtitle", String(length=255), nullable=False,index=False),
    Column("monthly_price", Integer, index=False, nullable=True),
    Column("annual_price", Integer, index=False, nullable=True),
    Column("monthly_requests_limit", Integer, index=False, nullable=True),
    Column("rate_limit", Integer, index=False, nullable=True),
    Column("rate_period", String(length=255), index=False, nullable=True),
    Column(
        "is_public",
        Boolean,
        index=True,
        nullable=False,
        server_default="true",
    ),
)

orm_registry.map_imperatively(SubscriptionPlan, subscription_plan_table)


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
