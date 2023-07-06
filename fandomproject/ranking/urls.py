from django.urls import path
from .views import RankingMain

app_name = 'ranking'

# Ranking app의 URL 패턴을 정의
urlpatterns = [
    path('', RankingMain.as_view(), name='index')            # views.py에 정의된 RankingMain 뷰를 호출 ranking app의 main url
]