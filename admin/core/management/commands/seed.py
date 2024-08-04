"""Seed the database with default data."""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Seed the database with default data."""

    def handle(self, *args, **options):
        """Handle the command."""
        self.stdout.write("Start database seeding...")
        self.stdout.write("Checking superuser...")
        self.initialize_superuser()
        self.stdout.write("Database seeding completed.")

    def initialize_superuser(self):
        """Create default superuser."""
        # check if superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser already exists.")
            return

        # get environment variables
        username = os.getenv("UNFOLD_SUPERUSER_USERNAME", None)
        email = os.getenv("UNFOLD_SUPERUSER_EMAIL", None)
        password = os.getenv("UNFOLD_SUPERUSER_PASSWORD", None)

        # if environment variables are not set, skip creating superuser
        if not all([username, email, password]):
            self.stdout.write(
                f"Superuser environment variables are not set. "
                f"Username env provided: {bool(username)}. "
                f"Email env provided: {bool(email)}. "
                f"Password env provided: {bool(password)}.",
            )
            return

        # create superuser if not exists
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write("Superuser created successfully.")
