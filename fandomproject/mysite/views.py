from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from accounts.models import User


# 메인화면
class Main(APIView):
    def get(self, request):
        print("로그인한 사용자" ,request.session['username'])

        username = request.session['username']

        User.objects.filter(username = username).first()

        return render(request, 'index.html')
