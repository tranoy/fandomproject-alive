from django.urls import path
from .views import Join,Login,Checkbox
from accounts.views import RequestPasswordResetEmail
from .views import  CompletePasswordReset, RequestPasswordResetEmail

app_name = 'accounts'

urlpatterns = [
    path('/', Login.as_view()),
    path('/join',Join.as_view()),
    path('/checkbox', Checkbox.as_view()),
    path('/set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),
    path('/request-reset-link', RequestPasswordResetEmail.as_view(), name="request-password"),
]