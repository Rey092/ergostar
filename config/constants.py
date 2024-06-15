"""Constants for the project."""

from __future__ import annotations

# Name of the favicon file in the static directory#
DB_SESSION_DEPENDENCY_KEY = "db_session"
# The name of the key used for dependency injection of the database session.#
USER_DEPENDENCY_KEY = "current_user"
# The name of the key used for storing DTO information.#
DTO_INFO_KEY = "info"
# Default page size to use.#
DEFAULT_PAGINATION_SIZE = 20
# Default cache key expiration in seconds.#
CACHE_EXPIRATION: int = 60
# The name of the default role assigned to all users.#
DEFAULT_USER_ROLE = "Application Access"
# The endpoint to use for the service health check.#
HEALTH_ENDPOINT = "/health"
# The site index URL.#
SITE_INDEX = "/"
# The URL path to use for the OpenAPI documentation.#
OPENAPI_SCHEMA = "/schema"
# The name of the superuser role.#
SUPERUSER_ACCESS_ROLE = "Superuser"
