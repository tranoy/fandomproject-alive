from django.urls import path
from .views import Join,Login,Checkbox

app_name = 'accounts'

urlpatterns = [
    path('', Login.as_view()),
    path('/join',Join.as_view()),
    path('/checkbox', Checkbox.as_view()),
]