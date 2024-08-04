"""Unfold configuration for Django admin."""

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": None,
    "SITE_HEADER": None,
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static(
            "favicon/android-chrome-512x512.png",
        ),  # light mode
        "dark": lambda request: static(
            "favicon/android-chrome-512x512.png",
        ),  # dark mode
    },
    "SITE_LOGO": {
        "light": lambda request: static(
            "favicon/android-chrome-512x512.png",
        ),  # light mode
        "dark": lambda request: static(
            "favicon/android-chrome-512x512.png",
        ),  # dark mode
    },
    "SITE_SYMBOL": "speed",  # symbol from an icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon/favicon.ico"),
        },
    ],
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "THEME": "dark",  # Force theme: "dark" or "light". Will disable theme switcher
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Навигация"),
                "items": [
                    {
                        "title": _("Подписки"),
                        "icon": "subscriptions",
                        "link": reverse_lazy(
                            "admin:core_subscriptionplansunfold_changelist",
                        ),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "core.subscriptionplansunfold",
            ],
            "items": [
                {
                    "title": _("Планы подписок"),
                    "link": reverse_lazy(
                        "admin:core_subscriptionplansunfold_changelist",
                    ),
                },
            ],
        },
    ],
}
