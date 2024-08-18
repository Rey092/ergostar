"""Compression configuration."""

from litestar.config.compression import CompressionConfig


def get_compression_config() -> CompressionConfig:
    """Get compression configuration."""
    return CompressionConfig(backend="gzip", gzip_compress_level=9)
