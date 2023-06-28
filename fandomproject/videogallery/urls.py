from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import GalleryMain,GalleryMore

app_name = 'videogallery'

urlpatterns = [
    path('', GalleryMain.as_view(), name='index'),
    path('/<int:pk>',GalleryMore.as_view(),name='more'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)