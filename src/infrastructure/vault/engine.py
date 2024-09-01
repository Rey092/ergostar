"""Vault configuration."""

from hvac import Client as VaultEngine

from src.main.config.settings import VaultSettings


def get_vault_engine(vault_settings: VaultSettings) -> VaultEngine:
    """Get redis engine."""
    engine = VaultEngine(
        url=vault_settings.URL,
        token=vault_settings.TOKEN,
        # TODO: add TLS
    )
    engine.session = None
    return engine
