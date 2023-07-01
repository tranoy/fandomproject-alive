from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render,redirect
from accounts.models import User
from making.models import TransformedLog

# 메인화면
class Main(APIView):
    def get(self, request):
        try:
            # 세션 데이터 가져오기
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
            print(user)
        except KeyError:
            nickname = None
            user = None
        transformItem = TransformedLog.objects.all()

        context = {'user': user,
                   'transformItem' : transformItem}
        
        return render(request, 'index.html', context)

# 로그아웃 시 세션 지워야 함
# 로그인 된 상태에서 로그아웃 누를 때
# /logout 경로 요청 시 LogOutClass get 함수 호출 하면서 세션 삭제하고 HOME 경로로 redirection
# 세션 삭제
class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return redirect("/")
    
class Privacy(APIView):
    def get(self,request):
        return render(request,'privacy.html')
class Policy(APIView):
    def get(self,request):
        return render(request,'policy.html')