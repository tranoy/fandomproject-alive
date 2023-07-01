from django.urls import path
from .views import Join,Login,Checkbox

## 추가
from django.contrib.auth import views as auth_views
from accounts.views import RequestPasswordResetEmail
from django.views.decorators.csrf import csrf_exempt

from .views import  CompletePasswordReset, RequestPasswordResetEmail
app_name = 'accounts'

urlpatterns = [
    path('/', Login.as_view()),
    path('/join',Join.as_view()),
    path('/checkbox', Checkbox.as_view()),
    ### 추가 부분
    path('/set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),
    path('/request-reset-link', RequestPasswordResetEmail.as_view(), name="request-password"),
]