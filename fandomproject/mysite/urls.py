from django.contrib import admin
from django.urls import path, include
from .views import Main





urlpatterns = [
    path('',Main.as_view()),
    path('login',include('accounts.urls')),
    path('making',include('making.urls')),
    path('ranking',include('ranking.urls')),
    path('board',include('board.urls',namespace="app_name")),
    path("videogallery",include('videogallery.urls')),
    path("admin", admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
