"""Shared utilities for the apps."""


def monkey_patch_advanced_alchemy():
    """Monkey patch advanced_alchemy."""
    from advanced_alchemy import base
    from sqlalchemy import FromClause

    base.FromClause = FromClause  # type: ignore[misc]
