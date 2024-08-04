from src.features.users.entities import User


class MockUserRepository:
    """Mock User Repository."""

    def __init__(self):
        """Initialize mock user repository."""
        self.users = [
            User(id=1, email="admin@example.com"),
        ]

    async def get_user(self) -> User:
        """Get a user by ID."""
        return self.users[0]
