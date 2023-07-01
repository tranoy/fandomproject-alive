from django.contrib import admin
from django.urls import path, include
from .views import Main,LogOut,Policy,Privacy


from accounts.views import CompletePasswordReset, RequestPasswordResetEmail


urlpatterns = [
    path('',Main.as_view(), name='main_index'),
    path('logout',LogOut.as_view()),
    path('challenge',include('challenge.urls')),
    path('login',include('accounts.urls')),
    path('making',include('making.urls')),
    path('ranking',include('ranking.urls')),
    path("videogallery",include('videogallery.urls')),
    path("privacy", Privacy.as_view()),
    path("policy", Policy.as_view()),
    path("admin/", admin.site.urls),
    #### 추가 부분
    path('/set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),
    path('/request-reset-link', RequestPasswordResetEmail.as_view(), name="request-password"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
