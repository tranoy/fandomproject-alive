from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ChallengeMain,ChallengeOne,ChallengeCompareResult

app_name = 'challenge'

# Challenge app의 Url패턴을 정의
urlpatterns = [
    path('',ChallengeMain.as_view(),name='index'),                                              # views.py에 정의된 ChallengeMain 뷰를 호출 challenge app의 main url
    path('/<int:pk>',ChallengeOne.as_view(),name='one'),                                        # views.py에 정의된 challengeOne 뷰를 호출, 정수 pk 변수로 전달되며 pk에 따라서 url이 대응
                                                                                                 # 해당 challenge id로 url 대응
    path('/<int:pk>/challenge_result', ChallengeCompareResult.as_view(), name='compare'),       # views.py에 정의된 challengeCompareResult 뷰를 호출, 정수 pk 변수로 전달되며 이에 대응
                                                                                                 # 사용자가 영상을 업로드한 후 결과를 확인할 수 있는 url
]   

# 개발 환경에서 미디어 파일에 접근할 수 있도록 하기위한 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)