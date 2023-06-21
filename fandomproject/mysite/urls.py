from django.contrib import admin
from django.urls import path, include
from .views import Main,LogOut





urlpatterns = [
    path('',Main.as_view()),
    path('logout',LogOut.as_view()),
    path('challenge',include('challenge.urls')),
    path('login',include('accounts.urls')),
    path('making',include('making.urls')),
    path('ranking',include('ranking.urls')),
    path("videogallery",include('videogallery.urls')),
    path("admin", admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
