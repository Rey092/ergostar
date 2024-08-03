"""Subscription models."""

from advanced_alchemy.base import orm_registry
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table

from src.features.subscriptions.entities import SubscriptionPlan

subscription_plan_table = Table(
    "subscriptions__plans",
    orm_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("title", String(length=255), nullable=False, index=False),
    Column("subtitle", String(length=255), nullable=False, index=False),
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
