from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ChallengeMain,ChallengeCompareResult,ChallengeOne

app_name = 'challenge'

urlpatterns = [
    path('',ChallengeMain.as_view(),name='index'),
    path('/1',ChallengeOne.as_view(),name='one'),
    path('/1/challenge_result', ChallengeCompareResult.as_view(), name='compare'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)