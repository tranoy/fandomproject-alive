from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from mysite.views import Main
app_name = 'making'

urlpatterns = [
    path('', views.index, name='index'),
    path('transform/', views.transform, name='transform'),
    path('display/', views.display, name='display'),
    path('download/', views.download, name='download'),
    path('post_image/', views.post_image, name='post_image'),  # post_image 뷰 함수에 해당하는 URL 패턴 추가
    #path('index/', views.BackIndex, name='backindex')


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
