"""URL configuration for an unfold admin project."""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from admin.config import settings

# add admin site
urlpatterns = [
    path("", admin.site.urls),
]

# add static and media files for development
if settings.DEBUG:
    media_urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    static_urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [*media_urlpatterns, *static_urlpatterns, *urlpatterns]
