"""Cache configuration."""

from litestar.config.response_cache import ResponseCacheConfig


def get_cache_config() -> ResponseCacheConfig:
    """Get cache configuration."""
    return ResponseCacheConfig()
