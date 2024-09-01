"""Subscription models."""

from datetime import UTC
from datetime import datetime

from advanced_alchemy.base import orm_registry
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import UUID
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from uuid_utils import uuid7

from src.domain.entities.subscriptions import SubscriptionPlan

# Define the table for the User model
subscription_plan_table = Table(
    # Table name
    "subscription_plans",
    # Metadata
    orm_registry.metadata,
    # Unique identifier for the user.
    Column("id", UUID, default=uuid7, primary_key=True, autoincrement=False),
    # Title of the subscription plan.
    Column("title", String(length=255), nullable=False),
    # Subtitle of the subscription plan.
    Column("subtitle", String(length=255), nullable=False),
    # Monthly price of the subscription plan. USD dollars.
    Column("monthly_price", Integer, nullable=True),
    # Annual price of the subscription plan. USD dollars.
    Column("annual_price", Integer, nullable=True),
    # Monthly requests limit of the subscription plan.
    Column("monthly_requests_limit", Integer, nullable=True),
    # Rate limit of the subscription plan. Works with rate_period.
    Column("rate_limit", Integer, nullable=True),
    # Rate period of the subscription plan. Works with rate_limit.
    # Examples: "1m" for 1 minute, "1h" for 1 hour,
    # "1d" for 1 day, "10s" for 10 seconds.
    Column("rate_period", String(length=255), nullable=False),
    # Is the subscription plan public? Public plans are visible to users.
    Column("is_public", Boolean, default=True, index=True, nullable=False),
    # Date/time of instance creation.
    Column(
        "created_at",
        DateTimeUTC(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    ),
    # Date/time of instance last update.
    Column(
        "updated_at",
        DateTimeUTC(timezone=True),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        nullable=False,
    ),
)


# Map the User class to the user_table
orm_registry.map_imperatively(
    SubscriptionPlan,
    subscription_plan_table,
)
