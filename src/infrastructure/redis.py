"""Redis engine configuration."""

from redis.asyncio import Redis

from src.main.config.settings import RedisSettings


def get_redis_engine(redis_settings: RedisSettings) -> Redis:
    """Get redis engine."""
    return Redis.from_url(
        url=redis_settings.URL,
        encoding="utf-8",
        decode_responses=False,
        socket_connect_timeout=redis_settings.SOCKET_CONNECT_TIMEOUT,
        socket_keepalive=redis_settings.SOCKET_KEEPALIVE,
        health_check_interval=redis_settings.HEALTH_CHECK_INTERVAL,
    )
