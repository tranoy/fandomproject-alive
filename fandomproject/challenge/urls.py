from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ChallengeMain,ChallengeOne,ChallengeCompareResult,Upload_success

app_name = 'challenge'

urlpatterns = [
    path('',ChallengeMain.as_view(),name='index'),
    path('/<int:pk>',ChallengeOne.as_view(),name='one'),
    path('/<int:pk>/upload_success', Upload_success.as_view(), name='upload_success'),
    path('/<int:pk>/challenge_result', ChallengeCompareResult.as_view(), name='compare'),
]
# path('/<int:pk>/upload',upload_video,name='upload1'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# 개발 환경에서만 media 파일을 제공하기 위한 설정