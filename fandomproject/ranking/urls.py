from django.urls import path
from .views import RankingMain

app_name = 'ranking'

urlpatterns = [
    path('', RankingMain.as_view(), name='index')
]