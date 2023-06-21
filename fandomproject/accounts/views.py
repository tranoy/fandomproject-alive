from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response

# Create your views here.


class Join(APIView):
    def get(self,request):
        return render(request, "accounts/join.html")
    
    def post(self,request):
        nickname = request.data.get('nickname',None)
        username = request.data.get('username',None)
        password1 = request.data.get('password1',None)
        password2 = request.data.get('password2')
        email = request.data.get('email','')

        # 비밀번호 일치하는지 확인
        if password1 == password2:
            User.objects.create(nickname=nickname,email=email,username=username,password=make_password(password1))
            # 로그인 정보 session에 저
            return redirect('/login')
        # 닉네임 중복여부 확인 

               
class Login(APIView):
    def get(self, request):
        return render(request, "accounts/login.html")
    def post(self,request):
        nickname = request.data.get('nickname',None)
        password = request.data.get('password',None)
        user = User.objects.filter(nickname=nickname).first()
        print(user)
        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # 로그인을 했다. 세션 or 쿠키에 삽입
            request.session['nickname'] = nickname
            return redirect('/')
        else:
             return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

class Checkbox(APIView):
    def get(self,request):
        return render(request,'accounts/checkbox.html')