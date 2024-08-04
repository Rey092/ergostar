"""Unfold admin configuration."""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .admins.subscrtiptions import *  # noqa: F403

# Unregister default User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)
