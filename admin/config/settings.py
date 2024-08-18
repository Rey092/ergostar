"""Django settings for unfold project."""

import binascii
import os
from pathlib import Path

from environ import Env

from admin.config.unfold import UNFOLD  # noqa: F401

# Environment
env = Env()

# Read environment variables from .env file
if env.bool("UNFOLD_READ_ENV_FILE", default=True):
    env.read_env(".env")

# Routes
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Basics
DEBUG = env.bool("UNFOLD_DEBUG", default=True)
ALLOWED_HOSTS = env.list("UNFOLD_ALLOWED_HOSTS", default=["*"])
SECRET_KEY = env.str(
    "UNFOLD_SECRET_KEY",
    default=binascii.hexlify(os.urandom(24)).decode(),
)

# Security
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# Application definition
INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin.core",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL Configuration
ROOT_URLCONF = "admin.config.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "admin.config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("UNFOLD_POSTGRES_DB"),
        "USER": env.str("UNFOLD_POSTGRES_USER"),
        "PASSWORD": env.str("UNFOLD_POSTGRES_PASSWORD"),
        "HOST": env.str("UNFOLD_POSTGRES_HOST", default="localhost"),
        "PORT": env.str("UNFOLD_POSTGRES_PORT", default="5432"),
    },
    "main": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = Path(BASE_DIR, "staticfiles/")
STATICFILES_DIRS = [
    Path(BASE_DIR, "static"),
]
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Media files
# https://docs.djangoproject.com/en/5.0/topics/files/
MEDIA_URL = "media/"
MEDIA_ROOT = Path(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database routing
# https://docs.djangoproject.com/en/5.0/topics/db/multi-db/#an-example
DATABASE_ROUTERS = ["admin.config.db_router.DatabaseRouter"]

# Logging
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
