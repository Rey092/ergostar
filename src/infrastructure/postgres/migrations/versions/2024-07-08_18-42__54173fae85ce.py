# type: ignore
"""

Revision ID: 54173fae85ce
Revises: 535d2890bb10
Create Date: 2024-07-08 18:42:56.985192+00:00

"""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from advanced_alchemy.types import EncryptedString, EncryptedText, GUID, ORA_JSONB, DateTimeUTC
from sqlalchemy import Text  # noqa: F401
from sqlalchemy.dialects import postgresql
if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ["downgrade", "upgrade", "schema_upgrades", "schema_downgrades", "data_upgrades", "data_downgrades"]

sa.GUID = GUID
sa.DateTimeUTC = DateTimeUTC
sa.ORA_JSONB = ORA_JSONB
sa.EncryptedString = EncryptedString
sa.EncryptedText = EncryptedText

# revision identifiers, used by Alembic.
revision = '54173fae85ce'
down_revision = '535d2890bb10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            schema_upgrades()
            data_upgrades()

def downgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            data_downgrades()
            schema_downgrades()

def schema_upgrades() -> None:
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriptions__plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_public', sa.Boolean(), server_default='true', nullable=False))
        batch_op.create_index(batch_op.f('ix_subscriptions__plans_is_public'), ['is_public'], unique=False)
        batch_op.drop_column('updated_at')
        batch_op.drop_column('is_available')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###

def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriptions__plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('is_available', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
        batch_op.drop_index(batch_op.f('ix_subscriptions__plans_is_public'))
        batch_op.drop_column('is_public')

    # ### end Alembic commands ###

def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""

def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""
