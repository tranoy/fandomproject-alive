from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import GalleryMain, GalleryMore

app_name = 'videogallery'

# Videogallery app의 URL패턴을 정의
urlpatterns = [
    path('', views.GalleryMain, name='index'),                  # views.py에 정의된 GalleryMain 함수 호출 videogallery app의 main url
    path('/<int:pk>/update', views.Edit, name='update'),        # views.py에 정의된 Edit 함수 호출, 수정할 때의 URL
    path('/<int:pk>', GalleryMore.as_view(), name='more'),      # views.py에 정의된 GalleryMore 뷰 호출, 자세히 보기의 URL
    path('/<int:pk>/delete', views.delete, name='delete')       # views.py에 정의된 delete 함수 호출, 삭제 시 URL
]

# 개발 환경에서 미디어 파일에 접근할 수 있도록 하기위한 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)