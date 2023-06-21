from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'),
    path('/<int:pk>',views.viewVideo, name='viewVideo'),
    path('/add', views.addVideo, name='addVideo'),
]