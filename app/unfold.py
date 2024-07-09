"""Django's admin app."""
import os
import logging
from pathlib import Path

from django.db import OperationalError

from app.multy import MultiDBModelAdmin
from config import settings

# prepare logger
logger = logging.getLogger(__name__)

# Configure settings before importing any Django components
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = settings.unfold.DEBUG
ALLOWED_HOSTS = settings.unfold.ALLOWED_HOSTS
SECRET_KEY = settings.unfold.SECRET_KEY
ROOT_URLCONF = __name__
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '__main__',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    "main": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.db.POSTGRES_DB,
        "USER": settings.db.POSTGRES_USER,
        "PASSWORD": settings.db.POSTGRES_PASSWORD,
        "HOST": settings.db.POSTGRES_HOST,
        "PORT": settings.db.POSTGRES_PORT,
    }
}
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
STATIC_URL = '/static/'
STATIC_PATH = os.path.join(BASE_DIR, 'static')

# Security
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# Setup Django
import django  # noqa

django.setup()

# Import Django components after setup
from django.contrib import admin  # noqa
from django.urls import path  # noqa
from django.core.wsgi import get_wsgi_application  # noqa
from django.contrib.auth.models import User  # noqa
from django.contrib.auth.models import Group  # noqa
from src.infrastructure.unfold.models import LandingHomePage  # noqa

# unregister default models
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(LandingHomePage)
class LandingHomePageAdmin(MultiDBModelAdmin):
    pass


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

urlpatterns = [
    path('', admin.site.urls),
]

# Create superuser
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
    else:
        logger.info('Superuser already exists')
except OperationalError:
    pass

application = get_wsgi_application()
