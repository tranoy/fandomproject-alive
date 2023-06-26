from django.shortcuts import render
from rest_framework.views import APIView
from .forms import VideoForm
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User

# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class ChallengeMain(APIView):
    def get(self,request):
        try:
            # 세션 데이터 가져오기
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
            print(user)
        except KeyError:
            nickname = None
            user = None
        return render(request, "challenge/challenge.html",context=dict(user=user))
    
class ChallengeOne(APIView):
    def get(self,request):
        return render(request,"challenge/ch1.html")
    
class ChallengeTwo(APIView):
    def get(self,request):
        return render(request,"challenge/ch2.html")
    
class ChallengeThree(APIView):
    def get(self,request):
        return render(request,"challenge/ch3.html")

    
class ChallegeUpload1(APIView):
    def get(self,request):
        return render(request,"challenge/ch1upload.html")
    def post(self, request):
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return Response({'video': video.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ChallengeCompareResult(APIView):
    def get(self, request):
        return render(request, "challenge/compare_result.html")


    
