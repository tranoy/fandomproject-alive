from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import GalleryMain, GalleryMore

app_name = 'videogallery'

urlpatterns = [
    path('', GalleryMain.as_view(), name='index'),
    path('/<int:pk>', GalleryMore.as_view(), name='more'),
    path('/<int:pk>/Edit', views.GoUpdate, name='goto_update'),
    #path('/<int:pk>/update', views.Edit, name='update'),
    path('/<int:pk>/update', GalleryMain.as_view(), name='update'),
    path('/<int:pk>/delete', views.delete, name='delete')
    #path('videogallery/', views.update_or_delete_row, name='videogallery'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)