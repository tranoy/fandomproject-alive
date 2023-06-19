from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ChallengeMain

app_name = 'challenge'

urlpatterns = [
    path('',ChallengeMain.as_view(),name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)