from django.urls import path
from . import views
from .views import Index

app_name = 'making'

urlpatterns = [
    path('', Index.as_view()),
    path('transform/', views.transform, name='transform'),  # 추가
    path('display/', views.display, name='display'),
]
