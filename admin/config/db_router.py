"""Unfold database-router."""

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models import Model


class DatabaseRouter:
    """A router to control all database operations on models."""

    unfold_models = [User, Permission, Group, ContentType, Session, LogEntry]

    def db_for_read(self, model: Model, **hints):
        """Attempts to read unfold models go to 'default'."""
        if model in self.unfold_models:
            return "default"
        return "main"

    def db_for_write(self, model, **hints):
        """Attempts to read unfold models go to 'default'."""
        if model in self.unfold_models:
            return "default"
        return "main"
